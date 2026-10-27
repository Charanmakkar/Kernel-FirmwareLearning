/* C60 reference: type:u8, length:u8, payload<=16; explicit reset after error.
 * feed consumes until input exhausted or failure. Callback receives borrowed bytes
 * valid only during the call. Callback failure latches failure; reset is required.
 */
#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
struct decoder {unsigned state;uint8_t type,length,have,payload[16];bool failed;};
typedef bool (*emit_fn)(void *,uint8_t,const uint8_t *,size_t);
void decoder_reset(struct decoder *d){memset(d,0,sizeof *d);}
bool decoder_feed(struct decoder *d,const uint8_t *p,size_t n,size_t *consumed,emit_fn emit,void *ctx){
    if(!d || (!p&&n) || !consumed || !emit)return false;
    *consumed=0;if(d->failed)return false;
    while(*consumed<n){
        uint8_t b=p[(*consumed)++];
        if(d->state==0){d->type=b;d->state=1;}
        else if(d->state==1){
            if(b>sizeof d->payload){d->failed=true;return false;}
            d->length=b;d->have=0;
            if(!b){if(!emit(ctx,d->type,d->payload,0)){d->failed=true;return false;}d->state=0;}
            else d->state=2;
        }else{
            d->payload[d->have++]=b;
            if(d->have==d->length){
                if(!emit(ctx,d->type,d->payload,d->length)){d->failed=true;return false;}
                d->state=0;
            }
        }
    }
    return true;
}
bool decoder_at_boundary(const struct decoder *d){return d && !d->failed && d->state==0;}
struct capture {unsigned count;uint8_t type[4],payload[4][16];size_t length[4];};
static bool capture(void *ctx,uint8_t type,const uint8_t *payload,size_t n){
    struct capture *c=ctx;if(c->count>=4)return false;
    unsigned i=c->count++;c->type[i]=type;c->length[i]=n;memcpy(c->payload[i],payload,n);return true;
}
int main(void){
    const uint8_t frame[]={1,3,'A','B','C'};size_t used;
    for(size_t split=0;split<=sizeof frame;split++){
        struct decoder d;decoder_reset(&d);struct capture c={0};
        assert(decoder_feed(&d,frame,split,&used,capture,&c)&&used==split);
        assert(decoder_feed(&d,frame+split,sizeof frame-split,&used,capture,&c));
        assert(c.count==1&&c.type[0]==1&&c.length[0]==3&&!memcmp(c.payload[0],"ABC",3));assert(decoder_at_boundary(&d));
    }
    struct decoder d;decoder_reset(&d);struct capture c={0};uint8_t two[]={1,3,'A','B','C',2,0};
    assert(decoder_feed(&d,two,sizeof two,&used,capture,&c)&&c.count==2&&c.length[1]==0);
    assert(decoder_feed(&d,NULL,0,&used,capture,&c)&&used==0);
    uint8_t bad[]={1,17,0};assert(!decoder_feed(&d,bad,sizeof bad,&used,capture,&c)&&used==2);
    assert(!decoder_feed(&d,frame,sizeof frame,&used,capture,&c)&&used==0);
    decoder_reset(&d);memset(&c,0,sizeof c);assert(decoder_feed(&d,frame,3,&used,capture,&c)&&c.count==0&&!decoder_at_boundary(&d));
    decoder_reset(&d);memset(&c,0,sizeof c);uint8_t full[18]={1,16};for(unsigned i=0;i<16;i++)full[i+2]=(uint8_t)i;
    assert(decoder_feed(&d,full,sizeof full,&used,capture,&c)&&c.length[0]==16&&c.payload[0][15]==15);
    puts("PASS: C60 all frame splits, zero-length record, coalesced frames, invalid length, latched error, reset, truncated state and maximum payload");return 0;
}
