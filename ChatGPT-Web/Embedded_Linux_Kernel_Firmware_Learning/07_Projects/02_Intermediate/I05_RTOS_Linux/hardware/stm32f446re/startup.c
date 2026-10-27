#include <stdint.h>
extern uint32_t _estack,_sidata,_sdata,_edata,_sbss,_ebss;
extern int main(void);
void vPortSVCHandler(void);void xPortPendSVHandler(void);void xPortSysTickHandler(void);
void Default_Handler(void){for(;;)__asm volatile("wfi");}
void Reset_Handler(void){
 uint32_t *src=&_sidata,*dst=&_sdata;
 while(dst<&_edata)*dst++=*src++;
 for(dst=&_sbss;dst<&_ebss;)*dst++=0;
 *(volatile uint32_t *)0xe000ed88 |= (0xfUL<<20); /* FPU CP10/CP11 */
 __asm volatile("dsb\nisb" ::: "memory");
 *(volatile uint32_t *)0xe000ed08 = 0x08000000; /* VTOR */
 (void)main();Default_Handler();
}
__attribute__((section(".isr_vector"),used))
void (*const vectors[112])(void)={
 [0]=(void (*)(void))&_estack,[1]=Reset_Handler,
 [2]=Default_Handler,[3]=Default_Handler,[4]=Default_Handler,
 [5]=Default_Handler,[6]=Default_Handler,[7]=0,[8]=0,[9]=0,[10]=0,
 [11]=vPortSVCHandler,[12]=Default_Handler,[13]=0,
 [14]=xPortPendSVHandler,[15]=xPortSysTickHandler,
 [16 ... 111]=Default_Handler
};
