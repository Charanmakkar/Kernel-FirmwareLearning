#include "util.h"
#include <string.h>
bool ring_init(struct ring *r, uint8_t *s, size_t n) {
    if (!r || !s || !n) return false;
    *r=(struct ring){.data=s,.capacity=n}; return true;
}
bool ring_push(struct ring *r, uint8_t v) {
    if (!r || r->count==r->capacity) return false;
    r->data[r->write_at]=v;
    r->write_at=(r->write_at+1u)%r->capacity; r->count++; return true;
}
bool ring_pop(struct ring *r, uint8_t *v) {
    if (!r || !v || !r->count) return false;
    *v=r->data[r->read_at];
    r->read_at=(r->read_at+1u)%r->capacity; r->count--; return true;
}
bool bit_assign(uint32_t *v, unsigned bit, bool on) {
    if (!v || bit>=32u) return false;
    uint32_t mask=UINT32_C(1)<<bit;
    *v=on ? (*v|mask) : (*v & ~mask); return true;
}
uint16_t crc16_ccitt(const uint8_t *p, size_t n) {
    uint16_t crc=0xffffu;
    for(size_t i=0;i<n;i++) {
        crc^=(uint16_t)((uint16_t)p[i]<<8);
        for(unsigned b=0;b<8;b++)
            crc=(uint16_t)((crc & 0x8000u) ? ((uint32_t)crc<<1)^0x1021u : (uint32_t)crc<<1);
    }
    return crc;
}
static void be16_put(uint8_t *p,uint16_t v) { p[0]=(uint8_t)(v>>8);p[1]=(uint8_t)v; }
static uint16_t be16_get(const uint8_t *p) { return (uint16_t)(((uint16_t)p[0]<<8)|p[1]); }
size_t frame_encode(const struct frame *f,uint8_t *p,size_t cap) {
    if(!f || !p || f->length>FRAME_MAX_PAYLOAD || cap<(size_t)f->length+10u) return 0;
    p[0]=0xa5;p[1]=0x5a;p[2]=1;p[3]=f->type;
    be16_put(p+4,f->length);be16_put(p+6,f->sequence);
    memcpy(p+8,f->payload,f->length);
    be16_put(p+8+f->length,crc16_ccitt(p+2,(size_t)f->length+6u));
    return (size_t)f->length+10u;
}
enum frame_result frame_decode(const uint8_t *p,size_t n,struct frame *f,size_t *used) {
    if (!used) return FRAME_INVALID;
    *used=0;
    if (!p || !f) return FRAME_INVALID;
    if (!n) return FRAME_MORE;
    if (p[0]!=0xa5 || (n>=2 && p[1]!=0x5a) || (n>=3 && p[2]!=1)) {
        *used=1;return FRAME_INVALID;
    }
    if (n<8) return FRAME_MORE;
    uint16_t length=be16_get(p+4);
    if (length>FRAME_MAX_PAYLOAD) { *used=1;return FRAME_INVALID; }
    size_t total=(size_t)length+10u;
    if(n<total) return FRAME_MORE;
    if(be16_get(p+8+length)!=crc16_ccitt(p+2,(size_t)length+6u)) {
        *used=1;return FRAME_INVALID;
    }
    f->type=p[3];f->sequence=be16_get(p+6);f->length=length;
    memcpy(f->payload,p+8,length);*used=total;return FRAME_OK;
}
