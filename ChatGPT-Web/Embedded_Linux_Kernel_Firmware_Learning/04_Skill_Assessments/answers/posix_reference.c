#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
/* Q061. Blocking descriptors only. Caller owns fd and SIGPIPE policy. */
int write_all_blocking(int fd,const void *buffer,size_t n){
    const unsigned char *p=buffer;
    if(!p&&n){errno=EINVAL;return -1;}
    while(n){
        size_t request=n>4096?4096:n;
        ssize_t wrote=write(fd,p,request);
        if(wrote>0){p+=(size_t)wrote;n-=(size_t)wrote;continue;}
        if(wrote<0&&errno==EINTR)continue;
        if(wrote==0)errno=EIO;
        return -1;
    }
    return 0;
}
int main(void){
    int pipefd[2];char out[16]={0};
    if(pipe(pipefd))return 1;
    if(write_all_blocking(pipefd[1],"reference",9))return 2;
    if(close(pipefd[1]))return 3;
    ssize_t n=read(pipefd[0],out,sizeof out);
    if(close(pipefd[0]))return 4;
    if(n!=9||memcmp(out,"reference",9))return 5;
    if(write_all_blocking(-1,"x",1)!=-1||errno!=EBADF)return 6;
    puts("PASS: Q061 blocking write helper normal pipe and invalid descriptor tests");
    return 0;
}
