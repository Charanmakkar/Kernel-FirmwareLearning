#define _POSIX_C_SOURCE 200809L
#include <pthread.h>
#include <signal.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <time.h>
#define CAPACITY 8u
struct sample { unsigned sensor,sequence; int value; };
static struct {
    pthread_mutex_t mutex;pthread_cond_t nonempty,nonfull;
    struct sample data[CAPACITY];unsigned head,tail,count,active;
    bool stop;unsigned long produced,consumed;
} q={.mutex=PTHREAD_MUTEX_INITIALIZER,.nonempty=PTHREAD_COND_INITIALIZER,
     .nonfull=PTHREAD_COND_INITIALIZER,.active=2};
struct producer_arg { unsigned sensor,samples,period_us; };
static sigset_t signal_set;
static void checked(int code) {if(code){fprintf(stderr,"pthread: %s\n",strerror(code));abort();}}
static void *producer(void *arg) {
    struct producer_arg *a=arg;
    for(unsigned i=0;i<a->samples;i++) {
        checked(pthread_mutex_lock(&q.mutex));
        while(q.count==CAPACITY&&!q.stop) checked(pthread_cond_wait(&q.nonfull,&q.mutex));
        if(q.stop){checked(pthread_mutex_unlock(&q.mutex));break;}
        q.data[q.tail]=(struct sample){a->sensor,i,(int)(a->sensor*100u+i%50u)};
        q.tail=(q.tail+1u)%CAPACITY;q.count++;q.produced++;
        checked(pthread_cond_signal(&q.nonempty));checked(pthread_mutex_unlock(&q.mutex));
        struct timespec pause={a->period_us/1000000u,(long)(a->period_us%1000000u)*1000};
        while(nanosleep(&pause,&pause)<0&&errno==EINTR){}
    }
    checked(pthread_mutex_lock(&q.mutex));q.active--;
    checked(pthread_cond_broadcast(&q.nonempty));checked(pthread_mutex_unlock(&q.mutex));return NULL;
}
static void *signal_thread(void *unused) {
    (void)unused;int sig;checked(sigwait(&signal_set,&sig));
    if(sig!=SIGUSR1){checked(pthread_mutex_lock(&q.mutex));q.stop=true;
        checked(pthread_cond_broadcast(&q.nonfull));checked(pthread_cond_broadcast(&q.nonempty));
        checked(pthread_mutex_unlock(&q.mutex));}
    return NULL;
}
static int number(const char *s,unsigned max,unsigned *out) {
    char *e;errno=0;unsigned long n=strtoul(s,&e,10);
    if(errno||e==s||*e||*s=='-'||n>max)return -1;
    *out=(unsigned)n;return 0;
}
int main(int argc,char **argv) {
    unsigned samples=100,period=1000;
    if(argc<2||argc>4||(argc>=3&&number(argv[2],1000000,&samples))||
       (argc==4&&number(argv[3],1000000,&period))){fprintf(stderr,"usage: %s OUTPUT.csv [SAMPLES_PER_SENSOR [PERIOD_US]]\n",argv[0]);return 2;}
    FILE *out=fopen(argv[1],"w");if(!out){perror("output");return 1;}
    sigemptyset(&signal_set);sigaddset(&signal_set,SIGINT);sigaddset(&signal_set,SIGTERM);sigaddset(&signal_set,SIGUSR1);
    checked(pthread_sigmask(SIG_BLOCK,&signal_set,NULL));
    pthread_t signals,workers[2];int err=pthread_create(&signals,NULL,signal_thread,NULL);
    if(err){fprintf(stderr,"signal thread: %s\n",strerror(err));fclose(out);return 1;}
    struct producer_arg args[2]={{0,samples,period},{1,samples,period}};unsigned started=0;int result=0;
    for(unsigned i=0;i<2;i++) {
        err=pthread_create(&workers[i],NULL,producer,&args[i]);
        if(err){fprintf(stderr,"producer: %s\n",strerror(err));result=1;
            checked(pthread_mutex_lock(&q.mutex));q.active-=2u-i;q.stop=true;
            checked(pthread_cond_broadcast(&q.nonfull));checked(pthread_mutex_unlock(&q.mutex));break;}
        started++;
    }
    if(fputs("sensor,sequence,value\n",out)==EOF) result=1;
    for(;;) {
        checked(pthread_mutex_lock(&q.mutex));
        if(result){q.stop=true;checked(pthread_cond_broadcast(&q.nonfull));}
        while(!q.count&&q.active) checked(pthread_cond_wait(&q.nonempty,&q.mutex));
        if(!q.count&&!q.active){checked(pthread_mutex_unlock(&q.mutex));break;}
        struct sample s=q.data[q.head];q.head=(q.head+1u)%CAPACITY;q.count--;
        checked(pthread_cond_signal(&q.nonfull));checked(pthread_mutex_unlock(&q.mutex));
        if(!result) {
            if(fprintf(out,"%u,%u,%d\n",s.sensor,s.sequence,s.value)<0||fflush(out)==EOF){perror("write");result=1;}
            else q.consumed++; /* Only the main thread accesses consumed until joins. */
        }
    }
    for(unsigned i=0;i<started;i++) checked(pthread_join(workers[i],NULL));
    /* SIGUSR1 wakes only the blocked signal monitor after finite completion. */
    err=pthread_kill(signals,SIGUSR1);if(err && err!=ESRCH) checked(err);
    checked(pthread_join(signals,NULL));
    if(fclose(out)==EOF){perror("close output");result=1;}
    fprintf(stderr,"produced=%lu consumed=%lu stop=%d\n",q.produced,q.consumed,q.stop);
    checked(pthread_cond_destroy(&q.nonempty));checked(pthread_cond_destroy(&q.nonfull));checked(pthread_mutex_destroy(&q.mutex));return result;
}
