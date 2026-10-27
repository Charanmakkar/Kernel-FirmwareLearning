/* Deliberately broken review fragment. Caller initializes mutex/condition.
 * count is the number of valid items; consumers hold q->mu on entry.
 * Do not execute as a complete program: the assessed defects are logical.
 */
#include <pthread.h>
struct queue {pthread_mutex_t mu;pthread_cond_t cv;unsigned count;int stopping;int item;};
int broken_take_locked(struct queue *q){
    if(q->count==0)pthread_cond_wait(&q->cv,&q->mu);
    q->count--;
    return q->item;
}
