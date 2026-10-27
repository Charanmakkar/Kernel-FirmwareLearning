#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <limits.h>
#include <dirent.h>
#include <ctype.h>
#include <unistd.h>
static int path(char *out,size_t n,const char *root,const char *pid,const char *leaf) {
    int used=snprintf(out,n,"%s/%s/%s",root,pid,leaf);
    return used<0 || (size_t)used>=n ? -1:0;
}
static void json_string(const char *p) {
    putchar('"');for(;*p;p++) {unsigned char c=(unsigned char)*p;
        if(c=='"'||c=='\\') printf("\\%c",c);
        else if(c<32) printf("\\u%04x",(unsigned)c);else putchar(c);
    }putchar('"');
}
static int unsigned_number(const char *s,unsigned long long *v) {
    if(!s || !*s || *s=='-') return -1;
    char *e;errno=0;*v=strtoull(s,&e,10);
    return errno || e==s || *e ? -1:0;
}
static long status_number(const char *s,int kib) {
    char *end;errno=0;long value=strtol(s,&end,10);
    if(errno||end==s||value<0)return -1;
    while(*end==' '||*end=='\t')end++;
    if(kib){if(strncmp(end,"kB",2))return -1;end+=2;}
    while(*end==' '||*end=='\t'||*end=='\n')end++;
    return *end ? -1:value;
}
int main(int argc,char **argv) {
    const char *root="/proc",*pid="self";
    if(argc==2) pid=argv[1];
    else if(argc==4 && !strcmp(argv[1],"--root")){root=argv[2];pid=argv[3];}
    else if(argc!=1){fprintf(stderr,"usage: %s [PID|self] or --root PROC_ROOT PID\n",argv[0]);return 2;}
    if(strcmp(pid,"self")) {unsigned long long p;if(unsigned_number(pid,&p)||p==0||p>INT_MAX){fputs("invalid PID\n",stderr);return 2;}}
    char filename[PATH_MAX];
    if(path(filename,sizeof filename,root,pid,"status")){fputs("path too long\n",stderr);return 1;}
    FILE *f=fopen(filename,"r");if(!f){perror(filename);return 1;}
    char *line=NULL;size_t cap=0;char name[256]="",state[256]="";long threads=-1,rss=-1;
    while(getline(&line,&cap,f)>=0) {
        if(!strncmp(line,"Name:",5)){snprintf(name,sizeof name,"%s",line+5);name[strcspn(name,"\n")]=0;}
        else if(!strncmp(line,"State:",6)){snprintf(state,sizeof state,"%s",line+6);state[strcspn(state,"\n")]=0;}
        else if(!strncmp(line,"Threads:",8)){threads=status_number(line+8,0);if(threads<1)threads=-1;}
        else if(!strncmp(line,"VmRSS:",6)){rss=status_number(line+6,1);}
    }
    int bad=ferror(f);fclose(f);free(line);line=NULL;cap=0;
    if(bad||!name[0]||!state[0]||threads<0){fputs("incomplete or malformed status\n",stderr);return 1;}
    if(path(filename,sizeof filename,root,pid,"stat")) return 1;
    f=fopen(filename,"r");if(!f){perror(filename);return 1;}
    ssize_t len=getline(&line,&cap,f);fclose(f);
    char *tail=len>0?strrchr(line,')'):NULL;
    if(!tail || tail[1]!=' '){free(line);fputs("malformed stat\n",stderr);return 1;}
    unsigned long long utime=0,stime=0;unsigned field=3;char *save=NULL;
    char *token=strtok_r(tail+2," \n",&save);int got_u=0,got_s=0;
    while(token) {
        if(field==14) got_u=unsigned_number(token,&utime)==0;
        if(field==15) {got_s=unsigned_number(token,&stime)==0;break;}
        field++;token=strtok_r(NULL," \n",&save);
    }
    free(line);if(!got_u||!got_s){fputs("missing CPU counters\n",stderr);return 1;}
    if(path(filename,sizeof filename,root,pid,"fd")) return 1;
    DIR *dir=opendir(filename);long fds=-1;
    if(dir){fds=0;struct dirent *entry;while((entry=readdir(dir))) if(strcmp(entry->d_name,".")&&strcmp(entry->d_name,"..")) fds++;closedir(dir);}
    printf("{\"pid\":");json_string(pid);printf(",\"name\":");json_string(name);
    printf(",\"state\":");json_string(state);
    printf(",\"threads\":%ld,\"rss_kib\":%ld,\"user_ticks\":%llu,\"system_ticks\":%llu,\"ticks_per_second\":%ld,\"open_fds\":%ld}\n",threads,rss,utime,stime,sysconf(_SC_CLK_TCK),fds);
    return ferror(stdout)?1:0;
}
