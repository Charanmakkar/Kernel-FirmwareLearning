#define _POSIX_C_SOURCE 200809L
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "protocol.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <signal.h>
static QueueHandle_t samples;
static int output_fd;
static volatile sig_atomic_t failed;
static TickType_t produced_at, transmitted_at;
static int stall;
struct sample {uint16_t seq;int32_t value;};
void vApplicationMallocFailedHook(void) {abort();}
void vApplicationStackOverflowHook(TaskHandle_t t,char *n) {(void)t;(void)n;abort();}
static void sensor(void *arg) {
 (void)arg;TickType_t tick=xTaskGetTickCount();
 for(uint16_t i=0;;i++) {
  if(stall && i==5) vTaskSuspend(NULL);
  struct sample s={i,25000+(int32_t)(i%10)*10};
  if(xQueueSend(samples,&s,0)!=pdPASS){failed=1;vTaskEndScheduler();}
  taskENTER_CRITICAL(); produced_at=xTaskGetTickCount(); taskEXIT_CRITICAL();
  vTaskDelayUntil(&tick,pdMS_TO_TICKS(50));
 }
}
static void serial_tx(void *arg) {
 (void)arg;struct sample s;
 for(;;) {
  if(xQueueReceive(samples,&s,pdMS_TO_TICKS(100))!=pdPASS)continue;
  uint8_t out[PACKET_SIZE];size_t done=0;packet(out,s.seq,s.value);
  TickType_t start=xTaskGetTickCount();
  while(done<sizeof out) {
   ssize_t n=write(output_fd,out+done,sizeof out-done);
   if(n>0){done+=(size_t)n;continue;}
   if(n<0 && errno==EINTR)continue;
   if(n<0 && (errno==EAGAIN||errno==EWOULDBLOCK)) {
    if(xTaskGetTickCount()-start>pdMS_TO_TICKS(100)){failed=1;vTaskEndScheduler();}
    vTaskDelay(pdMS_TO_TICKS(1));continue;
   }
   failed=1;vTaskEndScheduler();
  }
  taskENTER_CRITICAL(); transmitted_at=xTaskGetTickCount(); taskEXIT_CRITICAL();
  if(s.seq==19) vTaskEndScheduler();
 }
}
static void supervisor(void *arg) {
 (void)arg;
 for(;;) {
  TickType_t p,t,now=xTaskGetTickCount();
  taskENTER_CRITICAL(); p=produced_at; t=transmitted_at; taskEXIT_CRITICAL();
  if(now-p>pdMS_TO_TICKS(200)||now-t>pdMS_TO_TICKS(200)) {
   failed=1;vTaskEndScheduler();
  }
  vTaskDelay(pdMS_TO_TICKS(20));
 }
}
int main(int argc,char **argv) {
 if(argc<2||argc>3){fprintf(stderr,"usage: %s OUTPUT_FIFO [stall]\n",argv[0]);return 2;}
 stall=argc==3;
 signal(SIGPIPE,SIG_IGN);
 output_fd=open(argv[1],O_WRONLY|O_NONBLOCK);
 if(output_fd<0){perror("open output (reader must be ready)");return 1;}
 samples=xQueueCreate(4,sizeof(struct sample));
 if(!samples)return 1;
 if(xTaskCreate(sensor,"sensor",4096,NULL,2,NULL)!=pdPASS||
    xTaskCreate(serial_tx,"serial",4096,NULL,2,NULL)!=pdPASS||
    xTaskCreate(supervisor,"supervisor",4096,NULL,3,NULL)!=pdPASS)return 1;
 vTaskStartScheduler();
 close(output_fd);
 return failed?1:0;
}
