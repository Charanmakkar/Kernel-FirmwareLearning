/* Original reference solutions for Q021-Q040 and Q161-Q170.
 * C11 host logic only: no claim of hardware, ISR, or concurrent correctness.
 * Run: cc -std=c11 -Wall -Wextra -Werror -pedantic coding_reference.c -o coding_reference
 */
#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>

bool checked_mul(size_t a,size_t b,size_t *out){
    if(!out || (b && a>SIZE_MAX/b)) return false;
    *out=a*b; return true;
}
bool decode_be16(const uint8_t *p,size_t n,uint16_t *out){
    if(!p || n<2 || !out) return false;
    *out=(uint16_t)(((uint16_t)p[0]<<8)|p[1]); return true;
}
struct ring {uint8_t data[8]; size_t head,tail,count;};
bool ring_push(struct ring *r,uint8_t v){
    if(!r || r->count>=8) return false;
    r->data[r->head]=v; r->head=(r->head+1)%8; r->count++; return true;
}
bool ring_pop(struct ring *r,uint8_t *v){
    if(!r || !v || !r->count) return false;
    *v=r->data[r->tail]; r->tail=(r->tail+1)%8; r->count--; return true;
}
static int digit(char c){
    if(c>='0'&&c<='9') return c-'0';
    if(c>='a'&&c<='f') return c-'a'+10;
    if(c>='A'&&c<='F') return c-'A'+10;
    return -1;
}
bool hex_decode(const char *s,uint8_t *out,size_t cap,size_t *used){
    if(!s || !used) return false;
    size_t n=strlen(s);
    if(n%2 || n/2>cap || (!out&&n)) return false;
    for(size_t i=0;i<n;i++) if(digit(s[i])<0) return false;
    for(size_t i=0;i<n/2;i++) out[i]=(uint8_t)((digit(s[2*i])<<4)|digit(s[2*i+1]));
    *used=n/2; return true;
}
bool reverse_bytes(uint8_t *p,size_t n){
    if(!p&&n) return false;
    for(size_t i=0;i<n/2;i++){uint8_t t=p[i];p[i]=p[n-1-i];p[n-1-i]=t;}
    return true;
}
bool bit_assign(uint32_t *v,unsigned bit,bool on){
    if(!v || bit>=32) return false;
    uint32_t m=UINT32_C(1)<<bit;
    if(on) *v|=m; else *v&=~m;
    return true;
}
uint16_t crc16_ccitt(const uint8_t *p,size_t n){
    assert(p || n==0);
    uint16_t crc=0xffff;
    for(size_t i=0;i<n;i++){
        crc^=(uint16_t)((uint16_t)p[i]<<8);
        for(unsigned b=0;b<8;b++) crc=(uint16_t)((crc&0x8000)?(crc<<1)^0x1021:crc<<1);
    }
    return crc;
}
bool parse_u32(const char *s,uint32_t *out){
    if(!s || !*s || !out) return false;
    uint32_t v=0;
    for(;*s;s++){
        if(*s<'0'||*s>'9') return false;
        uint32_t d=(uint32_t)(*s-'0');
        if(v>(UINT32_MAX-d)/10) return false;
        v=v*10+d;
    }
    *out=v; return true;
}
bool copy_text(char *out,size_t cap,const char *s,size_t *needed){
    if(!s || !needed || (!out&&cap)) return false;
    size_t n=strlen(s); *needed=n;
    if(cap){size_t take=n<cap-1?n:cap-1;memcpy(out,s,take);out[take]='\0';}
    return n<cap;
}
uint32_t saturating_add(uint32_t a,uint32_t b){return a>UINT32_MAX-b?UINT32_MAX:a+b;}
struct debounce {bool stable,candidate; unsigned count;};
bool debounce_step(struct debounce *d,bool sample,unsigned threshold){
    assert(d && threshold>0);
    if(sample==d->stable){d->candidate=sample;d->count=0;return d->stable;}
    if(sample!=d->candidate){d->candidate=sample;d->count=1;}
    else if(d->count<threshold) d->count++;
    if(d->count>=threshold){d->stable=sample;d->count=0;}
    return d->stable;
}
struct average {uint32_t values[4];uint64_t sum;unsigned count,next;};
uint32_t average_push(struct average *a,uint32_t x){
    assert(a && a->count<=4 && a->next<4);
    if(a->count==4)a->sum-=a->values[a->next];else a->count++;
    a->values[a->next]=x;a->sum+=x;a->next=(a->next+1)%4;
    return (uint32_t)(a->sum/a->count);
}
bool sorted_insert(uint32_t *a,size_t *n,size_t cap,uint32_t v){
    if(!a || !n || *n>=cap) return false;
    size_t i=*n;
    while(i && a[i-1]>v){a[i]=a[i-1];i--;}
    a[i]=v;(*n)++;return true;
}
bool tick_due(uint32_t now,uint32_t deadline){return (uint32_t)(now-deadline)<UINT32_C(0x80000000);}
struct node {struct node *next;};
bool list_has_cycle(const struct node *head){
    const struct node *slow=head,*fast=head;
    while(fast && fast->next){slow=slow->next;fast=fast->next->next;if(slow==fast)return true;}
    return false;
}
unsigned popcount32(uint32_t x){unsigned n=0;while(x){x&=x-1;n++;}return n;}
bool round_up(size_t n,size_t alignment,size_t *out){
    if(!out || !alignment || (alignment&(alignment-1)) || n>SIZE_MAX-(alignment-1))return false;
    *out=(n+alignment-1)&~(alignment-1);return true;
}
bool validate_tlvs(const uint8_t *p,size_t n,size_t *records){
    if(!records || (!p&&n))return false;
    size_t i=0,c=0;
    while(i<n){if(n-i<2)return false;size_t len=p[i+1];i+=2;if(len>n-i)return false;i+=len;c++;}
    *records=c;return true;
}
bool alarm_step(bool old,int32_t value,int32_t low,int32_t high,bool *out){
    if(!out || low>=high)return false;
    *out=value>=high?true:value<=low?false:old;return true;
}
bool field_replace(uint32_t *p,unsigned offset,unsigned width,uint32_t value){
    if(!p || !width || width>32 || offset>32-width)return false;
    uint32_t mask=width==32?UINT32_MAX:(UINT32_C(1)<<width)-1;
    if(value>mask)return false;
    *p=(*p&~(mask<<offset))|(value<<offset);return true;
}
/* Q161-Q170 */
bool seq_newer(uint16_t candidate,uint16_t previous){
    uint16_t d=(uint16_t)(candidate-previous);return d!=0 && d<0x8000;
}
bool escape_frame(const uint8_t *p,size_t n,uint8_t *out,size_t cap,size_t *used){
    if((!p&&n) || !out || !used || n>(SIZE_MAX-2)/2 || cap<2*n+2)return false;
    size_t j=0;out[j++]=0x7e;
    for(size_t i=0;i<n;i++){
        if(p[i]==0x7e||p[i]==0x7d){out[j++]=0x7d;out[j++]=(uint8_t)(p[i]^0x20);}
        else out[j++]=p[i];
    }
    out[j++]=0x7e;*used=j;return true;
}
struct heartbeats {uint32_t last[3];bool seen[3];};
bool supervisor_ok(const struct heartbeats *h,uint32_t now,const uint32_t timeout[3]){
    if(!h||!timeout)return false;
    for(unsigned i=0;i<3;i++)if(!h->seen[i] || (uint32_t)(now-h->last[i])>timeout[i])return false;
    return true;
}
enum control_state {DISARMED,ARMED,FAULT};
enum control_event {ARM,DISARM,COMMAND,TIMEOUT,FAULT_EVENT,CLEAR_FAULT};
enum control_state control_step(enum control_state s,enum control_event e,bool *motion_allowed){
    assert(motion_allowed);
    if(e==FAULT_EVENT)s=FAULT;
    else if(s==FAULT){if(e==CLEAR_FAULT)s=DISARMED;}
    else if(e==DISARM||e==TIMEOUT)s=DISARMED;
    else if(e==ARM)s=ARMED;
    *motion_allowed=(s==ARMED);return s;
}
bool sensor_valid(bool status,int32_t value,int32_t low,int32_t high,uint32_t stamp,uint32_t now,uint32_t max_age){
    return status && low<=high && value>=low && value<=high && (uint32_t)(now-stamp)<=max_age;
}
uint32_t retry_delay(uint32_t initial,unsigned attempt,uint32_t cap){
    if(initial>=cap)return cap;
    uint32_t d=initial;
    while(attempt-- && d<cap){if(d>cap/2)return cap;d*=2;if(d==0)break;}
    return d;
}
int32_t median3(int32_t a,int32_t b,int32_t c){
    int32_t t;if(a>b){t=a;a=b;b=t;}if(b>c){t=b;b=c;c=t;}if(a>b){t=a;a=b;b=t;}return b;
}
bool scale_i32(int32_t x,int32_t numerator,int32_t denominator,int32_t *out){
    if(!out || denominator<=0)return false;
    int64_t value=(int64_t)x*numerator/denominator;
    if(value<INT32_MIN || value>INT32_MAX)return false;
    *out=(int32_t)value;return true;
}
int32_t decode_s12(uint16_t container){int32_t v=container&0x0fff;return v>=2048?v-4096:v;}
struct bucket {uint32_t tokens,capacity,interval,last,suppressed;};
bool bucket_take(struct bucket *b,uint32_t now){
    assert(b && b->interval && b->tokens<=b->capacity);
    uint32_t elapsed=now-b->last,refill=elapsed/b->interval;
    b->last+=refill*b->interval;
    if(refill>b->capacity-b->tokens)b->tokens=b->capacity;else b->tokens+=refill;
    if(!b->tokens){if(b->suppressed<UINT32_MAX)b->suppressed++;return false;}
    b->tokens--;return true;
}
int main(void){
    size_t z=99,n=0;uint16_t u16=99;uint32_t u32=99;bool flag=false;
    assert(checked_mul(0,SIZE_MAX,&z)&&z==0);assert(checked_mul(SIZE_MAX,1,&z)&&z==SIZE_MAX);assert(!checked_mul(SIZE_MAX,2,&z)&&z==SIZE_MAX);
    uint8_t be[]={0x12,0x34};assert(decode_be16(be,2,&u16)&&u16==4660);assert(!decode_be16(be,1,&u16)&&u16==4660);
    struct ring r={0};uint8_t b;for(unsigned i=0;i<8;i++)assert(ring_push(&r,(uint8_t)i));assert(!ring_push(&r,9));for(unsigned i=0;i<3;i++){assert(ring_pop(&r,&b));assert(b==i);}for(unsigned i=8;i<11;i++)assert(ring_push(&r,(uint8_t)i));for(unsigned i=3;i<11;i++){assert(ring_pop(&r,&b));assert(b==i);}assert(!ring_pop(&r,&b));
    uint8_t hex[3]={9,9,9};assert(hex_decode("00aF",hex,3,&n)&&n==2&&hex[1]==0xaf);assert(!hex_decode("0G",hex,3,&n)&&hex[1]==0xaf);assert(!hex_decode("0",hex,3,&n));assert(!hex_decode("0000",hex,1,&n));
    uint8_t rev[]={1,2,3,4,5};assert(reverse_bytes(NULL,0));assert(reverse_bytes(rev,5)&&rev[0]==5&&rev[4]==1);assert(reverse_bytes(rev,5)&&rev[0]==1);
    u32=0;assert(bit_assign(&u32,31,true)&&u32==0x80000000);assert(!bit_assign(&u32,32,true));assert(bit_assign(&u32,31,false)&&u32==0);
    assert(crc16_ccitt((const uint8_t*)"123456789",9)==0x29b1);assert(crc16_ccitt(NULL,0)==0xffff);
    assert(parse_u32("4294967295",&u32)&&u32==UINT32_MAX);assert(!parse_u32("4294967296",&u32)&&u32==UINT32_MAX);assert(!parse_u32("",&u32));assert(!parse_u32("12x",&u32));assert(!parse_u32("-1",&u32));
    char txt[4];assert(copy_text(txt,4,"abc",&n)&&n==3);assert(!copy_text(txt,4,"abcd",&n)&&n==4&&!strcmp(txt,"abc"));assert(!copy_text(NULL,0,"",&n)&&n==0);
    assert(saturating_add(UINT32_MAX,1)==UINT32_MAX);assert(saturating_add(2,3)==5);
    struct debounce db={0};bool samples[]={0,1,0,1,1,1};for(unsigned i=0;i<6;i++)assert(debounce_step(&db,samples[i],3)==(i==5));
    struct average av={0};uint32_t in[]={4,8,12,16,20},expected[]={4,6,8,10,14};for(unsigned i=0;i<5;i++)assert(average_push(&av,in[i])==expected[i]);
    uint32_t sorted[4];n=0;assert(sorted_insert(sorted,&n,4,5));assert(sorted_insert(sorted,&n,4,1));assert(sorted_insert(sorted,&n,4,5));assert(sorted_insert(sorted,&n,4,3));assert(!sorted_insert(sorted,&n,4,0));assert(sorted[0]==1&&sorted[1]==3&&sorted[2]==5&&sorted[3]==5);
    assert(!tick_due(0xffffffef,0xfffffff0));assert(tick_due(0xfffffff0,0xfffffff0));assert(tick_due(0x10,0xfffffff0));
    struct node a={0},c={0};a.next=&c;assert(!list_has_cycle(&a));c.next=&a;assert(list_has_cycle(&a));assert(!list_has_cycle(NULL));
    assert(popcount32(0)==0&&popcount32(UINT32_MAX)==32&&popcount32(0x80000001)==2);
    assert(round_up(17,16,&z)&&z==32);assert(round_up(0,1,&z)&&z==0);assert(!round_up(SIZE_MAX,2,&z));assert(!round_up(5,3,&z));
    uint8_t tlv[]={1,0,2,2,9,8};assert(validate_tlvs(tlv,6,&n)&&n==2);assert(!validate_tlvs(tlv,5,&n));assert(!validate_tlvs(tlv,1,&n));assert(validate_tlvs(NULL,0,&n)&&n==0);
    assert(alarm_step(false,65,60,70,&flag)&&!flag);assert(alarm_step(flag,71,60,70,&flag)&&flag);assert(alarm_step(flag,68,60,70,&flag)&&flag);assert(alarm_step(flag,60,60,70,&flag)&&!flag);
    u32=0xffffffff;assert(field_replace(&u32,8,4,0)&&u32==0xfffff0ff);assert(!field_replace(&u32,31,2,1));assert(field_replace(&u32,0,32,0x12345678)&&u32==0x12345678);assert(!field_replace(&u32,0,4,16));
    assert(seq_newer(0,65535));assert(!seq_newer(65535,0));assert(!seq_newer(2,2));assert(!seq_newer(0x8000,0));
    uint8_t payload[]={0x7e,0x7d,1},encoded[8],enc_expected[]={0x7e,0x7d,0x5e,0x7d,0x5d,1,0x7e};assert(escape_frame(payload,3,encoded,8,&n)&&n==7&&!memcmp(encoded,enc_expected,7));assert(!escape_frame(payload,3,encoded,7,&n));
    struct heartbeats h={{10,20,30},{true,true,true}};uint32_t limits[]={50,50,50};assert(supervisor_ok(&h,40,limits));assert(!supervisor_ok(&h,61,limits));h.seen[1]=false;assert(!supervisor_ok(&h,40,limits));
    enum control_state state=DISARMED;state=control_step(state,ARM,&flag);assert(state==ARMED&&flag);state=control_step(state,TIMEOUT,&flag);assert(state==DISARMED&&!flag);state=control_step(state,FAULT_EVENT,&flag);state=control_step(state,ARM,&flag);assert(state==FAULT&&!flag);state=control_step(state,CLEAR_FAULT,&flag);assert(state==DISARMED&&!flag);
    assert(sensor_valid(true,10,0,10,100,150,50));assert(!sensor_valid(true,10,0,10,100,151,50));assert(!sensor_valid(false,5,0,10,100,100,50));
    assert(retry_delay(10,0,100)==10);assert(retry_delay(10,4,100)==100);assert(retry_delay(10,10000,100)==100);assert(retry_delay(0,100,100)==0);
    assert(median3(INT32_MIN,INT32_MAX,0)==0);assert(median3(3,2,1)==2);assert(median3(3,3,3)==3);
    int32_t signed_out;assert(scale_i32(-3,2,4,&signed_out)&&signed_out==-1);assert(!scale_i32(INT32_MAX,2,1,&signed_out));assert(!scale_i32(2,1,0,&signed_out));
    assert(decode_s12(0x7ff)==2047&&decode_s12(0x800)==-2048&&decode_s12(0xfff)==-1);
    struct bucket bk={2,2,10,0,0};assert(bucket_take(&bk,0));assert(bucket_take(&bk,0));assert(!bucket_take(&bk,0));assert(bucket_take(&bk,10));assert(!bucket_take(&bk,15));assert(bucket_take(&bk,100));assert(bk.suppressed==2);
    puts("PASS: 30 reference routines; boundary, invalid-input, wraparound and state-transition assertions completed");return 0;
}
