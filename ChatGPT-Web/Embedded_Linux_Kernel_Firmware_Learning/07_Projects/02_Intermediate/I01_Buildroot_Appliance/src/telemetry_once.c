#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/file.h>
#include <sys/stat.h>
#include <unistd.h>
static void crash(const char *point) {
    const char *v=getenv("LEARN_CRASH_AT");if(v && !strcmp(v,point))_exit(99);
}
static int write_all(int fd,const char *p,size_t n) {
    while(n){ssize_t k=write(fd,p,n);if(k<0&&errno==EINTR)continue;if(k<=0)return -1;p+=k;n-=(size_t)k;}return 0;
}
int main(int argc,char **argv) {
    if(argc!=2){fprintf(stderr,"usage: %s STATE_DIRECTORY\n",argv[0]);return 2;}
    int dir=open(argv[1],O_RDONLY|O_DIRECTORY|O_CLOEXEC);if(dir<0){perror("state directory");return 1;}
    int lock=openat(dir,"counter.lock",O_RDWR|O_CREAT|O_NOFOLLOW|O_CLOEXEC,0600);
    if(lock<0 || flock(lock,LOCK_EX)<0){perror("lock");if(lock>=0)close(lock);close(dir);return 1;}
    uint64_t value=0,check=0;int old=openat(dir,"counter",O_RDONLY|O_NOFOLLOW|O_CLOEXEC);int result=1;
    if(old>=0) {
        char buf[128];ssize_t used=0,k;
        while(used<(ssize_t)sizeof(buf)-1){k=read(old,buf+used,sizeof(buf)-1-(size_t)used);if(k<0&&errno==EINTR)continue;if(k<0){perror("read");close(old);goto done;}if(!k)break;used+=k;}
        close(old);buf[used]=0;
        char *end=NULL,*begin=buf+3;int invalid=strncmp(buf,"v1 ",3)!=0 || used==(ssize_t)sizeof(buf)-1;
        if(!invalid) {
            errno=0;
            if(*begin<'0'||*begin>'9') invalid=1;
            else {value=strtoull(begin,&end,10);invalid=errno || end==begin || *end!=' ';}
        }
        if(!invalid) {
            begin=end+1;errno=0;
            if(*begin<'0'||*begin>'9') invalid=1;
            else {check=strtoull(begin,&end,10);invalid=errno || end==begin || *end!='\n' || end[1]!=0;}
        }
        if(invalid || check!=(value^UINT64_C(0xa55aa55aa55aa55a))) {
            fputs("corrupt state; preserved for diagnosis\n",stderr);result=2;goto done;
        }
    } else if(errno!=ENOENT){perror("read state");goto done;}
    if(value==UINT64_MAX){fputs("counter exhausted\n",stderr);result=2;goto done;}
    value++;check=value^UINT64_C(0xa55aa55aa55aa55a);
    char data[128];int size=snprintf(data,sizeof data,"v1 %" PRIu64 " %" PRIu64 "\n",value,check);
    /* A directory-scoped lock serializes writers; stale temp is safe to replace. */
    int tmp=openat(dir,"counter.tmp",O_WRONLY|O_CREAT|O_TRUNC|O_NOFOLLOW|O_CLOEXEC,0600);
    if(tmp<0){perror("temporary file");goto done;}
    if(size<0 || (size_t)size>=sizeof data || write_all(tmp,data,(size_t)size)<0 || fsync(tmp)<0){perror("write/sync");close(tmp);goto done;}
    if(close(tmp)<0){perror("close");goto done;}crash("after_file_sync");
    if(renameat(dir,"counter.tmp",dir,"counter")<0){perror("rename");goto done;}crash("after_rename");
    if(fsync(dir)<0){perror("directory sync");goto done;}
    printf("{\"version\":1,\"counter\":%" PRIu64 "}\n",value);result=ferror(stdout)?1:0;
done:
    close(lock);close(dir);return result;
}
