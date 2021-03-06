# Generated by Django 2.2 on 2021-03-23 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_order', '0003_auto_20210324_0113'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_info',
            name='statuc',
            field=models.CharField(default='待确认', max_length=30, verbose_name='订单状态'),
        ),
        migrations.AlterField(
            model_name='price_model_info',
            name='level',
            field=models.IntegerField(choices=[(0, '默认'), (9, '最高级'), (1, '节假日'), (2, '自定义')], default=0, verbose_name='优先级'),
        ),
    ]
