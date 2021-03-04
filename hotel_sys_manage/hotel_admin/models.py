from django.contrib.auth.models import User
from django.db import models

# Create your models here.

manageFlag = True


class City_info(models.Model):
    '''
    国家编号	    countryId	Integer	无
    国家中文名	countryCn	String	无
    国家英文名	countryEn	String	无
    省份编号	    stateId	    Integer	无
    省份中文名	stateCn	    String	无
    省份英文名	stateEn	    String	无
    城市编号	    cityId	    Integer	无
    城市中文名	cityCn	    String	无
    城市英文名	cityEn	    String	无
    '''
    IS_EFFECTIVE = {
        (0, '不启用'),
        (1, '启用'),
    }
    cityId = models.IntegerField('城市编号', primary_key=True)
    cityCn = models.CharField('城市中文名', max_length=200, default='未知')
    cityEn = models.CharField('城市英文名', max_length=1000, default='未知')

    countryId = models.IntegerField('国家编号', default=0, )
    countryCn = models.CharField('国家中文名', max_length=20, default='未知')
    countryEn = models.CharField('国家英文名', max_length=200, default='未知')
    stateId = models.IntegerField('省份编号', default=0, )
    stateCn = models.CharField('省份中文名', max_length=200, default='未知')
    stateEn = models.CharField('省份英文名', max_length=1000, default='未知')
    is_effective = models.IntegerField('是否启用', default=0, choices=IS_EFFECTIVE)

    sys_create_time = models.DateTimeField('创建时间', auto_now_add=True)
    sys_update_time = models.DateTimeField('更新时间', auto_now=True)
    sys_create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')

    def __str__(self):
        return '[{}]-{}'.format(self.countryCn, self.cityCn)

    class Meta:
        managed = manageFlag
        verbose_name = '城市信息表'
        verbose_name_plural = verbose_name
        db_table = 'city_info'

class Hotel_info(models.Model):
    IS_EFFECTIVE = {
        (0, '不启用'),
        (1, '启用'),
    }

    hotelId = models.IntegerField('酒店编号', primary_key=True)
    countryId = models.IntegerField('国家编号', )
    stateId = models.IntegerField('省份编号', )
    cityId = models.IntegerField('城市编号', )
    ciyt_info = models.ForeignKey(City_info, null=True, on_delete=models.SET_NULL)
    star = models.IntegerField('酒店星级', default=0)
    hotelNameCn = models.CharField('酒店中文名', max_length=500, default='无')
    hotelNameEn = models.CharField('酒店英文名', max_length=1000, default='无')
    addressCn = models.CharField('中文地址', max_length=500, default='无')
    addressEn = models.CharField('英文地址', max_length=1000, default='无')
    phone = models.CharField('酒店总机', max_length=100, default='无')
    longitude = models.CharField('经度', max_length=20, default='无')
    latitude = models.CharField('纬度', max_length=20, default='无')
    instantConfirmation = models.IntegerField('是否即时确认', )
    sellType = models.IntegerField('是否热销酒店', )
    updateTime = models.CharField('酒店方的修改时间', max_length=100, default='无')

    is_effective = models.IntegerField('是否启用', default=0, choices=IS_EFFECTIVE)
    detail = models.TextField('备注')

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
        (0, '默认'),
        (1, '节假日'),
        (2, '自定义'),
        (9, '最高级'),
    }

    price_model_id = models.BigAutoField(primary_key=True)
    name = models.CharField('名称', max_length=100, default='无')
    proportion = models.DecimalField('加价比列', max_digits=5, decimal_places=2, default=1.0)
    level = models.IntegerField('优先级', default=0, choices=LEVEL_CHOICES)

    sys_create_time = models.DateTimeField('创建时间', auto_now_add=True)
    sys_update_time = models.DateTimeField('更新时间', auto_now=True)
    sys_create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')

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
