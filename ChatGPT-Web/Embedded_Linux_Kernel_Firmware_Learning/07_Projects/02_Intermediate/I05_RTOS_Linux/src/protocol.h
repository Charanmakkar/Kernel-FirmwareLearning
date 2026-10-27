#ifndef LEARNING_PROTOCOL_H
#define LEARNING_PROTOCOL_H
#include <stdint.h>
#include <stddef.h>
#define PACKET_SIZE 12
static inline uint16_t crc16(const uint8_t *p,size_t n) {
 uint16_t c=0xffff;
 while(n--) {c^=(uint16_t)*p++<<8;for(int b=0;b<8;b++)c=(c&0x8000)?(uint16_t)((c<<1)^0x1021):(uint16_t)(c<<1);}
 return c;
}
static inline void packet(uint8_t out[PACKET_SIZE],uint16_t seq,int32_t value) {
 uint32_t u=(uint32_t)value;
 out[0]='T';out[1]='L';out[2]=1;out[3]=1;
 out[4]=(uint8_t)(seq>>8);out[5]=(uint8_t)seq;
 for(int i=0;i<4;i++)out[6+i]=(uint8_t)(u>>(24-i*8));
 uint16_t c=crc16(out,10);out[10]=(uint8_t)(c>>8);out[11]=(uint8_t)c;
}
#endif
