#define _DEFAULT_SOURCE
#define _POSIX_C_SOURCE 200809L
#include "util.h"
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <poll.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>
#include <time.h>
#include <unistd.h>
static volatile sig_atomic_t interrupted;
static void on_signal(int signo) { interrupted=signo; }
static long long now_ms(void) {
    struct timespec t;if(clock_gettime(CLOCK_MONOTONIC,&t)<0) return -1;
    return (long long)t.tv_sec*1000+t.tv_nsec/1000000;
}
static int ready(int fd,short events,long long end) {
    for(;;) {
        if(interrupted){errno=EINTR;return -1;}
        long long now=now_ms();if(now<0) return -1;
        long long left=end-now;if(left<=0){errno=ETIMEDOUT;return -1;}
        struct pollfd p={.fd=fd,.events=events};
        int n=poll(&p,1,left>INT_MAX?INT_MAX:(int)left);
        if(n<0&&errno==EINTR) continue;
        if(n<0) return -1;
        if(n==0){errno=ETIMEDOUT;return -1;}
        if(p.revents&events) return 0;
        if(p.revents&(POLLERR|POLLHUP|POLLNVAL)){errno=EIO;return -1;}
    }
}
static int send_all(int fd,const uint8_t *p,size_t n,long long end) {
    size_t sent=0;
    while(sent<n) {
        if(ready(fd,POLLOUT,end)<0) return -1;
        ssize_t k=write(fd,p+sent,n-sent);
        if(k<0&&(errno==EINTR||errno==EAGAIN||errno==EWOULDBLOCK)) continue;
        if(k<=0){if(!k)errno=EIO;return -1;}sent+=(size_t)k;
    }return 0;
}
static int receive(int fd,struct frame *f,long long end) {
    uint8_t bytes[FRAME_MAX_SIZE];size_t have=0;
    for(;;) {
        if(ready(fd,POLLIN,end)<0) return -1;
        ssize_t k=read(fd,bytes+have,sizeof bytes-have);
        if(k<0&&(errno==EINTR||errno==EAGAIN||errno==EWOULDBLOCK)) continue;
        if(k<=0){if(!k)errno=EIO;return -1;}have+=(size_t)k;
        while(have) {
            size_t used=0;enum frame_result result=frame_decode(bytes,have,f,&used);
            if(result==FRAME_OK && f->sequence==1 && f->type==2) return 0;
            if(result==FRAME_MORE) break;
            if(!used || used>have){errno=EPROTO;return -1;}
            memmove(bytes,bytes+used,have-used);have-=used;
        }
    }
}
int main(int argc,char **argv) {
    if(argc!=4){fprintf(stderr,"usage: %s DEVICE PAYLOAD TIMEOUT_MS\n",argv[0]);return 2;}
    char *tail;errno=0;long timeout=strtol(argv[3],&tail,10);
    if(errno||*tail||tail==argv[3]||timeout<1||timeout>60000||strlen(argv[2])>FRAME_MAX_PAYLOAD){fputs("invalid payload or timeout\n",stderr);return 2;}
    struct sigaction action={0};action.sa_handler=on_signal;sigemptyset(&action.sa_mask);
    if(sigaction(SIGINT,&action,NULL)<0 || sigaction(SIGTERM,&action,NULL)<0 || sigaction(SIGHUP,&action,NULL)<0){perror("sigaction");return 1;}
    action.sa_handler=SIG_IGN;
    if(sigaction(SIGPIPE,&action,NULL)<0){perror("sigaction SIGPIPE");return 1;}
    int fd=open(argv[1],O_RDWR|O_NOCTTY|O_NONBLOCK|O_CLOEXEC);if(fd<0){perror("open");return 1;}
    struct termios original,raw;int changed=0,result=1;
    if(tcgetattr(fd,&original)<0){perror("tcgetattr");goto out;}
    /* Once original state is known, restore even when configuration fails. */
    changed=1;
    raw=original;cfmakeraw(&raw);raw.c_cflag|=CLOCAL|CREAD;raw.c_cflag&=~(CRTSCTS|CSTOPB);
    raw.c_cc[VMIN]=0;raw.c_cc[VTIME]=0;
    if(cfsetispeed(&raw,B115200)<0||cfsetospeed(&raw,B115200)<0||tcsetattr(fd,TCSANOW,&raw)<0){perror("termios");goto out;}
    struct frame request={.type=1,.sequence=1,.length=(uint16_t)strlen(argv[2])},response;
    memcpy(request.payload,argv[2],request.length);uint8_t bytes[FRAME_MAX_SIZE];
    size_t n=frame_encode(&request,bytes,sizeof bytes);long long start=now_ms();
    if(start<0||send_all(fd,bytes,n,start+timeout)<0||receive(fd,&response,start+timeout)<0){perror("transaction");goto out;}
    if(fwrite(response.payload,1,response.length,stdout)!=response.length||putchar('\n')==EOF||fflush(stdout)==EOF){perror("stdout");goto out;}
    result=0;
out:
    if(changed){
        int restored;
        do {restored=tcsetattr(fd,TCSANOW,&original);} while(restored<0&&errno==EINTR);
        if(restored<0){perror("restore termios");result=1;}
    }
    if(close(fd)<0){perror("close");result=1;}
    return interrupted ? 128+(int)interrupted:result;
}
