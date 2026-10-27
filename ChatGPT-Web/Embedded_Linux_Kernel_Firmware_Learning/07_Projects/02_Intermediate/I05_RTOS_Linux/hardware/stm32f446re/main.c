#include <stdint.h>
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "protocol.h"
#define REG32(a) (*(volatile uint32_t *)(a))
#define RCC 0x40023800UL
#define GPIOA 0x40020000UL
#define UART 0x40004400UL
#define IWDG 0x40003000UL
static QueueHandle_t queue;
static TickType_t produced,transmitted;
struct sample {uint16_t seq;int32_t temperature;};
void lab_assert(void){__asm volatile("cpsid i");for(;;)__asm volatile("wfi");}
void vApplicationMallocFailedHook(void){lab_assert();}
void vApplicationStackOverflowHook(TaskHandle_t t,char*n){(void)t;(void)n;lab_assert();}
static void board_init(void){
 REG32(RCC)|=1U;while(!(REG32(RCC)&2U)){}
 REG32(RCC+8)&=~3U;while(REG32(RCC+8)&12U){}
 REG32(RCC+8)&=~((15U<<4)|(7U<<10)|(7U<<13)); /* HCLK/APB at HSI 16MHz */
 REG32(RCC+0x30)|=1U;REG32(RCC+0x40)|=1U<<17;
 (void)REG32(RCC+0x40);
 REG32(GPIOA)=(REG32(GPIOA)&~((3U<<4)|(3U<<6)))|(2U<<4)|(2U<<6);
 REG32(GPIOA+0x20)=(REG32(GPIOA+0x20)&~((15U<<8)|(15U<<12)))|(7U<<8)|(7U<<12);
 REG32(UART+0x0c)=0;REG32(UART+8)=139; /* 16MHz / 115200, oversample 16 */
 REG32(UART+0x10)=0;REG32(UART+0x14)=0;
 REG32(UART+0x0c)=(1U<<13)|(1U<<3)|(1U<<2);
 REG32(0xe000ed0c)=0x05fa0000U; /* PRIGROUP 0: all implemented bits preemption */
 /* Independent watchdog: nominal ~2 s at 32 kHz LSI; characterize tolerance. */
 REG32(IWDG)=0xcccc;REG32(IWDG)=0x5555;REG32(IWDG+4)=6;REG32(IWDG+8)=250;
 while(REG32(IWDG+0x0c)){}
 REG32(IWDG)=0xaaaa;
}
static void sensor(void *arg){
 (void)arg;TickType_t tick=xTaskGetTickCount();
 for(uint16_t seq=0;;seq++){
#ifdef INJECT_STALL
  if(seq==5)vTaskSuspend(NULL);
#endif
  struct sample s={seq,25000+(int32_t)(seq%10)*10};
  if(xQueueSend(queue,&s,0)!=pdPASS)lab_assert();
  taskENTER_CRITICAL();produced=xTaskGetTickCount();taskEXIT_CRITICAL();
  vTaskDelayUntil(&tick,pdMS_TO_TICKS(50));
 }
}
static void transmit(void *arg){
 (void)arg;struct sample s;
 for(;;){
  if(xQueueReceive(queue,&s,pdMS_TO_TICKS(100))!=pdPASS)continue;
  uint8_t bytes[PACKET_SIZE];packet(bytes,s.seq,s.temperature);
  TickType_t start=xTaskGetTickCount();
  for(unsigned i=0;i<PACKET_SIZE;i++){
   while(!(REG32(UART)&(1U<<7))){
    if(xTaskGetTickCount()-start>pdMS_TO_TICKS(100))lab_assert();
    vTaskDelay(1);
   }
   REG32(UART+4)=bytes[i];
  }
  taskENTER_CRITICAL();transmitted=xTaskGetTickCount();taskEXIT_CRITICAL();
 }
}
static void supervise(void *arg){
 (void)arg;
 for(;;){
  TickType_t p,t,now=xTaskGetTickCount();
  taskENTER_CRITICAL();p=produced;t=transmitted;taskEXIT_CRITICAL();
  if(now-p>pdMS_TO_TICKS(200)||now-t>pdMS_TO_TICKS(200))lab_assert();
  REG32(IWDG)=0xaaaa;
  vTaskDelay(pdMS_TO_TICKS(20));
 }
}
int main(void){
 board_init();queue=xQueueCreate(4,sizeof(struct sample));configASSERT(queue);
 configASSERT(xTaskCreate(sensor,"sensor",256,0,2,0)==pdPASS);
 configASSERT(xTaskCreate(transmit,"uart",256,0,2,0)==pdPASS);
 configASSERT(xTaskCreate(supervise,"health",256,0,3,0)==pdPASS);
 vTaskStartScheduler();lab_assert();return 0;
}
