#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <poll.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
static long long ms(void){struct timespec t;if(clock_gettime(CLOCK_MONOTONIC,&t))return -1;return (long long)t.tv_sec*1000+t.tv_nsec/1000000;}
static int transfer(int fd,char *buf,size_t n,int writing){
    size_t done=0;long long start=ms();if(start<0)return -1;
    while(done<n){long long left=start+2000-ms();if(left<=0){errno=ETIMEDOUT;return -1;}
        struct pollfd p={.fd=fd,.events=writing?POLLOUT:POLLIN};int r=poll(&p,1,(int)left);
        if(r<0&&errno==EINTR)continue;
        if(r<=0){if(!r)errno=ETIMEDOUT;return -1;}
        if(p.revents&(POLLERR|POLLHUP|POLLNVAL)){errno=EIO;return -1;}
        ssize_t k=writing?write(fd,buf+done,n-done):read(fd,buf+done,n-done);
        if(k<0&&(errno==EINTR||errno==EAGAIN))continue;
        if(k<=0){if(!k)errno=EIO;return -1;}done+=(size_t)k;
    }return 0;
}
int main(int argc,char **argv){
    if(argc!=3||strlen(argv[2])>1024){fprintf(stderr,"usage: %s DEVICE TEXT (max 1024 bytes)\n",argv[0]);return 2;}
    int fd=open(argv[1],O_RDWR|O_NONBLOCK|O_CLOEXEC);if(fd<0){perror("open");return 1;}
    size_t n=strlen(argv[2]);char buf[1025];int result=1;
    if(transfer(fd,argv[2],n,1)<0||transfer(fd,buf,n,0)<0){perror("I/O");goto out;}
    buf[n]=0;if(memcmp(buf,argv[2],n)){fputs("mismatch: requires exclusive test access to empty FIFO\n",stderr);goto out;}
    puts(buf);result=0;
out:close(fd);return result;
}
