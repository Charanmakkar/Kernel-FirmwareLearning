#include <errno.h>
#include <stdint.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
static uint64_t sum_to(unsigned n) {
    uint64_t sum=0;for(unsigned i=1;i<=n;i++)sum+=i;return sum;
}
int main(int argc,char **argv) {
    if(argc!=2){fprintf(stderr,"usage: %s N (0..1000000)\n",argv[0]);return 2;}
    char *end;errno=0;unsigned long n=strtoul(argv[1],&end,10);
    if(errno||end==argv[1]||*end||*argv[1]=='-'||n>1000000){fputs("invalid N\n",stderr);return 2;}
#if defined(__aarch64__)
    const char *arch="aarch64";
#elif defined(__x86_64__)
    const char *arch="x86_64";
#else
    const char *arch="other";
#endif
    printf("arch=%s pointer_bytes=%zu n=%lu sum=%" PRIu64 "\n",arch,sizeof(void*),n,sum_to((unsigned)n));
    return ferror(stdout)?1:0;
}
