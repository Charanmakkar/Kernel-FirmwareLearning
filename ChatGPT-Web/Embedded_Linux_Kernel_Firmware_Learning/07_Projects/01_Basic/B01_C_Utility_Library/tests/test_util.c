#include "util.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
int main(void) {
    struct ring r;uint8_t storage[3],v;
    assert(!ring_init(&r,storage,0));assert(ring_init(&r,storage,3));
    assert(!ring_pop(&r,&v));
    for(unsigned cycle=0;cycle<1000;cycle++) {
        assert(ring_push(&r,1));assert(ring_push(&r,2));assert(ring_push(&r,3));
        assert(!ring_push(&r,4));
        for(unsigned k=1;k<=3;k++) {assert(ring_pop(&r,&v));assert(v==k);}
        assert(!ring_pop(&r,&v));
    }
    uint32_t bits=0;assert(bit_assign(&bits,31,true));assert(bits==UINT32_C(0x80000000));
    assert(!bit_assign(&bits,32,true));assert(bit_assign(&bits,31,false));assert(!bits);
    assert(crc16_ccitt((const uint8_t*)"123456789",9)==0x29b1);
    uint8_t wire[FRAME_MAX_SIZE];struct frame in={.type=7,.sequence=0x1234},out;
    for(unsigned len=0;len<=FRAME_MAX_PAYLOAD;len++) {
        in.length=(uint16_t)len;for(unsigned j=0;j<len;j++) in.payload[j]=(uint8_t)j;
        size_t n=frame_encode(&in,wire,sizeof wire),used=99;
        assert(n==len+10u);assert(frame_encode(&in,wire,n-1u)==0);
        for(size_t cut=0;cut<n;cut++) {assert(frame_decode(wire,cut,&out,&used)==FRAME_MORE);assert(!used);}
        assert(frame_decode(wire,n,&out,&used)==FRAME_OK && used==n);
        assert(out.length==len && out.type==7 && out.sequence==0x1234);
        assert(!memcmp(in.payload,out.payload,len));
        wire[n-1]^=1;assert(frame_decode(wire,n,&out,&used)==FRAME_INVALID && used==1);
    }
    wire[0]=0xa5;wire[1]=0x5a;wire[2]=1;wire[4]=0xff;wire[5]=0xff;
    size_t used;assert(frame_decode(wire,8,&out,&used)==FRAME_INVALID);
    /* Deterministic malformed-byte sweep exercises parser bounds. */
    uint32_t rng=1;
    for(unsigned i=0;i<10000;i++) {
        for(size_t j=0;j<sizeof wire;j++){rng=rng*1664525u+1013904223u;wire[j]=(uint8_t)(rng>>24);}
        enum frame_result x=frame_decode(wire,i%sizeof wire,&out,&used);
        assert(x==FRAME_INVALID || x==FRAME_MORE || x==FRAME_OK);
    }
    puts("PASS ring wrap/full/empty; bits; CRC known vector; 129 frame lengths; truncation; corruption; 10000 malformed inputs");
}
