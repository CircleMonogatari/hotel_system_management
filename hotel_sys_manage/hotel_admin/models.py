from django.contrib.auth.models import User
from django.db import models

# Create your models here.

manageFlag = True


class Hotel_info(models.Model):
    hotel_id = models.BigAutoField(primary_key=True)
    name = models.CharField('名称', max_length=100, default='无')
    city = models.CharField('城市', max_length=50, default='未知')
    address = models.CharField('地址', max_length=200, default='未知')

    # detail = models.TextField('备注') #TODO: 后边加

    sys_create_time = models.DateTimeField('创建时间', auto_now_add=True)
    sys_update_time = models.DateTimeField('更新时间', auto_now=True)
    sys_create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')

    class Meta:
        managed = manageFlag
        verbose_name = '酒店信息表'
        verbose_name_plural = verbose_name
        db_table = 'hotel_info'


class Price_model_info(models.Model):
    LEVEL_CHOICES = {
        ('0', '默认'),
        ('1', '节假日'),
        ('2', '自定义'),
        ('9', '最高级'),
    }

    price_model_id = models.BigAutoField(primary_key=True)
    name = models.CharField('名称', max_length=100, default='无')
    proportion = models.DecimalField('加价比列', max_digits=5, decimal_places=2, default=1.0)
    level = models.IntegerField('优先级', default=0, choices=LEVEL_CHOICES)

    class Meta:
        managed = manageFlag
        verbose_name = '加价类型表'
        verbose_name_plural = verbose_name
        db_table = 'price_model_info'


class Room_info(models.Model):
    room_id = models.BigAutoField(primary_key=True)
    room_type = models.CharField('房型', max_length=100, default='无')
    hotel = models.ForeignKey(Hotel_info, on_delete=models.SET_NULL, null=True, verbose_name='酒店')

    price = models.DecimalField('报价', max_digits=5, decimal_places=2, default=0.0)
    custom_proce = models.DecimalField('强制自定义售价', max_digits=5, decimal_places=2, default=0.0)
    price_model = models.ManyToManyField(Price_model_info, verbose_name='加价类型')

    sys_create_time = models.DateTimeField('创建时间', auto_now_add=True)
    sys_update_time = models.DateTimeField('更新时间', auto_now=True)
    sys_create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')

    class Meta:
        managed = manageFlag
        verbose_name = '房间信息表'
        verbose_name_plural = verbose_name
        db_table = 'room_info'


class Order_info(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    room_type = models.CharField('房型', max_length=100, default='无')
    hotel = models.ForeignKey(Hotel_info, on_delete=models.SET_NULL, null=True, verbose_name='酒店')
    channel = models.CharField('渠道', max_length=100, )

    price = models.DecimalField('报价', max_digits=5, decimal_places=2, default=0.0)
    custom_proce = models.DecimalField('强制自定义售价', max_digits=5, decimal_places=2, default=0.0)
    price_model = models.ManyToManyField(Price_model_info, verbose_name='加价类型')

    sys_create_time = models.DateTimeField('创建时间', auto_now_add=True)
    sys_update_time = models.DateTimeField('更新时间', auto_now=True)
    sys_create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')

    class Meta:
        managed = manageFlag
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name
        db_table = 'order_info'
