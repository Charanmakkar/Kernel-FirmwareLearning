// SPDX-License-Identifier: GPL-2.0-only
#include <linux/module.h>
#include <linux/of.h>
#include <linux/platform_device.h>
#include <linux/gpio/consumer.h>
#include <linux/interrupt.h>
#include <linux/atomic.h>
#include <linux/sysfs.h>
struct edge_counter { atomic64_t edges; struct gpio_desc *input; };
static irqreturn_t edge_irq(int irq, void *arg)
{
 struct edge_counter *s = arg;
 atomic64_inc(&s->edges);
 return IRQ_HANDLED;
}
static ssize_t edges_show(struct device *dev, struct device_attribute *a, char *buf)
{
 struct edge_counter *s = dev_get_drvdata(dev);
 return sysfs_emit(buf, "%lld\n", (long long)atomic64_read(&s->edges));
}
static DEVICE_ATTR_RO(edges);
static struct attribute *edge_attrs[] = { &dev_attr_edges.attr, NULL };
static const struct attribute_group edge_group = { .attrs = edge_attrs };
static int edge_probe(struct platform_device *pdev)
{
 struct device *dev = &pdev->dev;
 struct edge_counter *s;
 int irq, ret;
 s = devm_kzalloc(dev, sizeof(*s), GFP_KERNEL);
 if (!s) return -ENOMEM;
 atomic64_set(&s->edges, 0);
 s->input = devm_gpiod_get(dev, "event", GPIOD_IN);
 if (IS_ERR(s->input))
  return dev_err_probe(dev, PTR_ERR(s->input), "event GPIO unavailable\n");
 irq = gpiod_to_irq(s->input);
 if (irq < 0) return dev_err_probe(dev, irq, "no GPIO IRQ\n");
 platform_set_drvdata(pdev, s);
 ret = devm_request_threaded_irq(dev, irq, NULL, edge_irq,
        IRQF_TRIGGER_RISING | IRQF_ONESHOT, dev_name(dev), s);
 if (ret) return dev_err_probe(dev, ret, "IRQ request failed\n");
 /* Last acquired, first released: sysfs removed before IRQ/state disappear. */
 return devm_device_add_group(dev, &edge_group);
}
static const struct of_device_id edge_of_match[] = {
 { .compatible = "learning,gpio-edge-counter" }, { }
};
MODULE_DEVICE_TABLE(of, edge_of_match);
static struct platform_driver edge_driver = {
 .probe = edge_probe,
 .driver = { .name = "learning-edge-counter", .of_match_table = edge_of_match }
};
module_platform_driver(edge_driver);
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Educational rising-edge GPIO counter for Linux 6.12");
