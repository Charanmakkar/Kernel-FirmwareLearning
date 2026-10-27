#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <signal.h>
#include <time.h>
#include <errno.h>
static volatile sig_atomic_t stop;
static void halt(int sig) { (void)sig; stop=1; }
int main(void) {
 struct sigaction a={0}; a.sa_handler=halt; sigemptyset(&a.sa_mask);
 if(sigaction(SIGTERM,&a,0)<0||sigaction(SIGINT,&a,0)<0)return 1;
 setvbuf(stdout,NULL,_IOLBF,0);
 for(unsigned long n=0;!stop;n++) {
  struct timespec now,delay={1,0};
  if(clock_gettime(CLOCK_MONOTONIC,&now))return 1;
  if(printf("seq=%lu monotonic_s=%lld source=simulated\n",n,(long long)now.tv_sec)<0)return 1;
  while(nanosleep(&delay,&delay)&&errno==EINTR&&!stop){}
 }
 return 0;
}
