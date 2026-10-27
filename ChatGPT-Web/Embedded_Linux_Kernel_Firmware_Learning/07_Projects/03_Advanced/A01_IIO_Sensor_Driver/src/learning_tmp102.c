// SPDX-License-Identifier: GPL-2.0-only
#include <linux/module.h>
#include <linux/of.h>
#include <linux/i2c.h>
#include <linux/iio/iio.h>
#include <linux/delay.h>
#include <linux/bitops.h>
#define REG_TEMP 0x00
#define REG_CONFIG 0x01
#define CFG_SHUTDOWN BIT(8)
#define CFG_EXTENDED BIT(4)
struct tmp_state { struct i2c_client *client; u16 original; };
static void restore_config(void *data)
{
 struct tmp_state *s = data;
 int ret = i2c_smbus_write_word_swapped(s->client, REG_CONFIG, s->original);
 if (ret) dev_warn(&s->client->dev, "config restore failed: %d\n", ret);
}
static int tmp_read_raw(struct iio_dev *indio, const struct iio_chan_spec *chan,
                       int *val, int *val2, long mask)
{
 struct tmp_state *s = iio_priv(indio);
 int ret;
 switch (mask) {
 case IIO_CHAN_INFO_RAW:
  ret = i2c_smbus_read_word_swapped(s->client, REG_TEMP);
  if (ret < 0) return ret;
  *val = sign_extend32((u16)ret >> 4, 11);
  return IIO_VAL_INT;
 case IIO_CHAN_INFO_SCALE:
  /* Temperature IIO scale is in millidegrees Celsius per raw count. */
  *val = 62; *val2 = 500000;
  return IIO_VAL_INT_PLUS_MICRO;
 default: return -EINVAL;
 }
}
static const struct iio_info tmp_info = { .read_raw = tmp_read_raw };
static const struct iio_chan_spec tmp_channels[] = {
 { .type = IIO_TEMP, .info_mask_separate = BIT(IIO_CHAN_INFO_RAW) | BIT(IIO_CHAN_INFO_SCALE) }
};
static int tmp_probe(struct i2c_client *client)
{
 struct iio_dev *indio;
 struct tmp_state *s;
 int ret;
 if (!i2c_check_functionality(client->adapter, I2C_FUNC_SMBUS_WORD_DATA))
  return -EOPNOTSUPP;
 indio = devm_iio_device_alloc(&client->dev, sizeof(*s));
 if (!indio) return -ENOMEM;
 s = iio_priv(indio); s->client = client;
 ret = i2c_smbus_read_word_swapped(client, REG_CONFIG);
 if (ret < 0) return dev_err_probe(&client->dev, ret, "read config\n");
 s->original = ret;
 ret = i2c_smbus_write_word_swapped(client, REG_CONFIG,
       s->original & ~(CFG_EXTENDED | CFG_SHUTDOWN));
 if (ret < 0) return dev_err_probe(&client->dev, ret, "write config\n");
 ret = devm_add_action_or_reset(&client->dev, restore_config, s);
 if (ret) return ret;
 msleep(35);
 indio->name = "learning_tmp102";
 indio->info = &tmp_info;
 indio->modes = INDIO_DIRECT_MODE;
 indio->channels = tmp_channels;
 indio->num_channels = ARRAY_SIZE(tmp_channels);
 return devm_iio_device_register(&client->dev, indio);
}
static const struct of_device_id tmp_of[] = {
 { .compatible = "learning,tmp102" }, { }
};
MODULE_DEVICE_TABLE(of, tmp_of);
static const struct i2c_device_id tmp_ids[] = { { "learning_tmp102", 0 }, { } };
MODULE_DEVICE_TABLE(i2c, tmp_ids);
static struct i2c_driver tmp_driver = {
 .driver = { .name = "learning_tmp102", .of_match_table = tmp_of },
 .probe = tmp_probe, .id_table = tmp_ids
};
module_i2c_driver(tmp_driver);
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Educational TMP102 IIO direct mode driver Linux 6.12");
