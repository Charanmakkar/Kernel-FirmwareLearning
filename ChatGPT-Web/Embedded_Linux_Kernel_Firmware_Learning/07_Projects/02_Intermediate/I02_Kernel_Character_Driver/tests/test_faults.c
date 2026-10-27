#define _GNU_SOURCE
#include <assert.h>
#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <unistd.h>

static void drain(int fd)
{
    char b[512];
    while (read(fd,b,sizeof b)>0) {}
    assert(errno==EAGAIN);
}
static void on_signal(int signal_number) { (void)signal_number; }
int main(void)
{
    int fd=open("/dev/learn_fifo",O_RDWR|O_NONBLOCK);
    assert(fd>=0);
    drain(fd);
    long page=sysconf(_SC_PAGESIZE);
    assert(page>128);
    char *memory=mmap(NULL,(size_t)page*2,PROT_READ|PROT_WRITE,
                      MAP_PRIVATE|MAP_ANONYMOUS,-1,0);
    assert(memory!=MAP_FAILED);
    assert(mprotect(memory+page,(size_t)page,PROT_NONE)==0);
    char sent[128],received[128];
    memset(sent,'Q',sizeof sent);
    assert(write(fd,sent,sizeof sent)==(ssize_t)sizeof sent);
    errno=0;
    assert(read(fd,memory+page,4)==-1 && errno==EFAULT);
    /* No readable destination bytes: the FIFO data must remain intact. */
    assert(read(fd,received,sizeof received)==(ssize_t)sizeof received);
    assert(memcmp(received,sent,sizeof sent)==0);
    errno=0;
    assert(write(fd,memory+page,4)==-1 && errno==EFAULT);
    errno=0;
    assert(read(fd,received,1)==-1 && errno==EAGAIN);
    assert(write(fd,sent,sizeof sent)==(ssize_t)sizeof sent);
    errno=0;
    ssize_t copied=read(fd,memory+page-64,sizeof sent);
    /* Architecture-dependent partial progress is permitted; verify reported
       progress and remaining data agree rather than assuming a copy chunk. */
    assert((copied==-1 && errno==EFAULT) || (copied>0 && copied<=64));
    size_t prefix=copied>0?(size_t)copied:0;
    if(prefix) assert(memcmp(memory+page-64,sent,prefix)==0);
    assert(read(fd,received,sizeof received)==(ssize_t)(sizeof sent-prefix));
    assert(memcmp(received,sent+prefix,sizeof sent-prefix)==0);
    assert(munmap(memory,(size_t)page*2)==0);
    close(fd);

    /* With no SA_RESTART and no data, SIGALRM must interrupt the wait. */
    pid_t child=fork();
    assert(child>=0);
    if(child==0){
        struct sigaction action={0};action.sa_handler=on_signal;
        sigemptyset(&action.sa_mask);
        assert(sigaction(SIGALRM,&action,NULL)==0);
        int blocking=open("/dev/learn_fifo",O_RDONLY);assert(blocking>=0);
        alarm(1);errno=0;char one;
        ssize_t count=read(blocking,&one,1);
        int ok=count==-1 && errno==EINTR;
        close(blocking);_exit(ok?0:1);
    }
    int status;assert(waitpid(child,&status,0)==child);
    assert(WIFEXITED(status)&&WEXITSTATUS(status)==0);
    puts("PASS no-progress EFAULT; partial copy accounting; interrupted blocked read");
    return 0;
}
