/* Deliberately broken assessment input. Review before execution. */
#include <stddef.h>
#include <stdint.h>
#include <string.h>
int parse_payload(const uint8_t *input,size_t available,uint8_t output[16]){
    size_t length=input[0];
    memcpy(output,input+1,length);
    return available>=length+1?0:-1;
}
