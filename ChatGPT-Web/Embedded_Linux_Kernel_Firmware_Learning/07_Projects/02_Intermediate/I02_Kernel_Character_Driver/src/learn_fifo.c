// SPDX-License-Identifier: GPL-2.0-only
/* Linux 6.12 educational byte-stream FIFO; not a hardware driver. */
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/miscdevice.h>
#include <linux/kfifo.h>
#include <linux/mutex.h>
#include <linux/poll.h>
#include <linux/wait.h>
#include <linux/atomic.h>
#define FIFO_BYTES 4096
static DECLARE_KFIFO(buffer, unsigned char, FIFO_BYTES);
static DEFINE_MUTEX(buffer_lock);
static DECLARE_WAIT_QUEUE_HEAD(readers);
static DECLARE_WAIT_QUEUE_HEAD(writers);
/* Readiness snapshot; FIFO indices themselves are accessed under the mutex. */
static atomic_t available = ATOMIC_INIT(0);

static ssize_t learn_read(struct file *file, char __user *dst, size_t count,
			  loff_t *offset)
{
	unsigned int copied = 0;
	int ret;
	(void)offset;
	if (!count)
		return 0;
	for (;;) {
		ret = mutex_lock_interruptible(&buffer_lock);
		if (ret)
			return ret;
		if (!kfifo_is_empty(&buffer))
			break;
		mutex_unlock(&buffer_lock);
		if (file->f_flags & O_NONBLOCK)
			return -EAGAIN;
		ret = wait_event_interruptible(readers, atomic_read(&available) > 0);
		if (ret)
			return ret;
	}
	/* uaccess can fault/sleep; a mutex is permitted here, not a spinlock. */
	ret = kfifo_to_user(&buffer, dst, min_t(size_t, count, FIFO_BYTES), &copied);
	atomic_set(&available, kfifo_len(&buffer));
	mutex_unlock(&buffer_lock);
	if (copied)
		wake_up_interruptible(&writers);
	return copied ? (ssize_t)copied : ret;
}

static ssize_t learn_write(struct file *file, const char __user *src,
			   size_t count, loff_t *offset)
{
	unsigned int copied = 0;
	int ret;
	(void)offset;
	if (!count)
		return 0;
	for (;;) {
		ret = mutex_lock_interruptible(&buffer_lock);
		if (ret)
			return ret;
		if (!kfifo_is_full(&buffer))
			break;
		mutex_unlock(&buffer_lock);
		if (file->f_flags & O_NONBLOCK)
			return -EAGAIN;
		ret = wait_event_interruptible(writers,
			atomic_read(&available) < FIFO_BYTES);
		if (ret)
			return ret;
	}
	ret = kfifo_from_user(&buffer, src, min_t(size_t, count, FIFO_BYTES), &copied);
	atomic_set(&available, kfifo_len(&buffer));
	mutex_unlock(&buffer_lock);
	if (copied)
		wake_up_interruptible(&readers);
	return copied ? (ssize_t)copied : ret;
}

static __poll_t learn_poll(struct file *file, poll_table *wait)
{
	__poll_t mask = 0;
	int used;
	poll_wait(file, &readers, wait);
	poll_wait(file, &writers, wait);
	used = atomic_read(&available);
	if (used)
		mask |= EPOLLIN | EPOLLRDNORM;
	if (used < FIFO_BYTES)
		mask |= EPOLLOUT | EPOLLWRNORM;
	return mask;
}

static const struct file_operations learn_fops = {
	.owner = THIS_MODULE,
	.open = stream_open,
	.read = learn_read,
	.write = learn_write,
	.poll = learn_poll,
	.llseek = NULL,
};
static struct miscdevice learn_device = {
	.minor = MISC_DYNAMIC_MINOR,
	.name = "learn_fifo",
	.fops = &learn_fops,
	.mode = 0600,
};
static int __init learn_init(void)
{
	INIT_KFIFO(buffer);
	return misc_register(&learn_device);
}
static void __exit learn_exit(void)
{
	/* .owner prevents normal unload while any open file pins this module. */
	misc_deregister(&learn_device);
}
module_init(learn_init);
module_exit(learn_exit);
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Teaching FIFO with blocking I/O, nonblocking I/O and poll");
