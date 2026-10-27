/* DBG01 repair: length:u8 then exactly that many available payload bytes.
 * Extra input is allowed; caller can consume length+1. Output changes on success only.
 */
#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
int parse_payload(const uint8_t *input,size_t available,uint8_t output[16],size_t *used){
    if(!input || !output || !used || available<1)return -1;
    size_t length=input[0];
    if(length>16 || length>available-1)return -1;
    memcpy(output,input+1,length);*used=length;return 0;
}
int main(void){
    uint8_t out[16]={9};size_t used=99;uint8_t short_header[]={4},good[]={2,'A','B'},big[18]={17},truncated[]={3,'A'};
    assert(parse_payload(NULL,0,out,&used)==-1&&used==99&&out[0]==9);
    assert(parse_payload(short_header,1,out,&used)==-1&&used==99&&out[0]==9);
    assert(parse_payload(big,18,out,&used)==-1&&used==99&&out[0]==9);
    assert(parse_payload(truncated,2,out,&used)==-1&&used==99&&out[0]==9);
    assert(parse_payload(good,3,out,&used)==0&&used==2&&out[0]=='A'&&out[1]=='B');
    puts("PASS: DBG01 bounds and unchanged-failure contract");return 0;
}
