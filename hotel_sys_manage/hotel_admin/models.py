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

    # static field
    themeType = models.CharField('酒店主题', max_length=500, default='无')  # vacation	见常量列表
    area = models.IntegerField('行政区', default=-1)  # 30000184
    businessCircle = models.IntegerField('商业区', default=-1)  # 30001724
    fax = models.CharField('传真', max_length=100, default='无')  # 00623-61761868
    email = models.CharField('邮箱', max_length=500, default='无')  #
    postCode = models.CharField('邮编号', max_length=100, default='无')  #
    checkPolicy = models.CharField('酒店入离政策', max_length=500, default='无')  # 入住时间:14点以后，离店时间:12点以前
    childrenPolicy = models.CharField('儿童政策', max_length=100, default='无')  # 不接受18岁以下客人单独入住。
    petPolicy = models.CharField('宠物政策', max_length=100, default='无')  # 不可携带宠物。
    establishmentDate = models.CharField('开业时间', max_length=200, default='无')  #
    renovationDate = models.CharField('装修时间', max_length=200, default='无')  #
    hotelGroup = models.CharField('集团', max_length=500, default='无')  #
    hotelBrand = models.CharField('品牌', max_length=500, default='无')  #
    facilities = models.CharField('酒店设施', max_length=500, default='无')  # 11|12|13|14|15|17|18|19|20|22|23|24|21|73
    cardType = models.CharField('信用卡', max_length=500, default='无')  # Master,VISA,JCB,UnionPay,
    minPrice = models.DecimalField('酒店最低价', max_digits=5, decimal_places=2, default=0.0)  # 0
    introduceCn = models.CharField('酒店中文介绍', max_length=500, default='无')  #
    introduceEn = models.CharField('酒店英文介绍', max_length=500, default='无')  #

    sys_create_time = models.DateTimeField('创建时间', auto_now_add=True)
    sys_update_time = models.DateTimeField('更新时间', auto_now=True)
    sys_create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')

    class Meta:
        managed = manageFlag
        verbose_name = '酒店信息表'
        verbose_name_plural = verbose_name
        db_table = 'hotel_info'

    def set_puls_info(self, data):
        pass

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
    roomTypeId = models.IntegerField('房型编号', default=0)  # 无
    roomTypeCn = models.CharField('客房中文名称', max_length=50, default='无')  # 无
    roomTypeEn = models.CharField('客房英文名称', max_length=50, default='无')  # 无
    roomTypeEn = models.CharField('客房英文名称', max_length=50, default='无')  # 无
    basisroomid = models.IntegerField('基础房型ID', default=-1)  # 278954	基础房型仅供参考，无物理房型的，返回-1
    basisroomCn = models.CharField('基础房型中文名', max_length=50, default='无')  # 城景行政豪华房	基础房型仅供参考，无物理房型的，返回-1
    maximize = models.IntegerField('最大入住人数', default=-1)  # 无
    acreage = models.CharField('房间面积', max_length=50, default='无')  # 无
    bedWidth = models.CharField('床大小', max_length=50, default='无')  # 无
    floorDistribute = models.CharField('楼层', max_length=50, default='无')  # 无
    facilities = models.CharField('房型设施', max_length=50, default='无')  # 无
    extraBedtState = models.CharField('是否允许加床', max_length=50, default='无')  # 无
    bedCount = models.IntegerField('加床数量', default=-1)  # 无

    sys_create_time = models.DateTimeField('创建时间', auto_now_add=True)
    sys_update_time = models.DateTimeField('更新时间', auto_now=True)
    sys_create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')

    hotel = models.ForeignKey(Hotel_info, related_name='rooms', on_delete=models.CASCADE, verbose_name='酒店')

    class Meta:
        managed = manageFlag
        verbose_name = '房间信息表'
        verbose_name_plural = verbose_name
        db_table = 'room_info'


class Rate_info(models.Model):
    '''
    价格类型编号	rateTypeId	Integer	无
    价格类型中文名	rateTypeCn	String	无
    价格类型英文名	rateTypeEn	String  无
    '''
    rateTypeId = models.IntegerField('价格类型编号', primary_key=True)
    rateTypeCn = models.CharField('价格类型中文名', max_length=100)
    rateTypeEn = models.CharField('价格类型英文名', max_length=500)

    hotel = models.ForeignKey(Hotel_info, related_name='rates', on_delete=models.CASCADE, verbose_name='酒店')

    sys_create_time = models.DateTimeField('创建时间', auto_now_add=True)
    sys_update_time = models.DateTimeField('更新时间', auto_now=True)
    sys_create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')

    class Meta:
        managed = manageFlag
        verbose_name = '价格类型表'
        verbose_name_plural = verbose_name
        db_table = 'rate_info'


class Room_image_info(models.Model):
    '''
    图片编号	imageId	Integer	无
    图片类型	type	String	无	见常量列表
    图片关联房型	roomTypeIds	String	无	一张图片可能对应多个房型，多个逗号分隔。
    缩略图地址	thumbUrl	String	无
    图片地址	imageUrl	String	无
    是否带水印	imageLogo	Integer	无	0有水印logo 1无水印logo
    图片规格	imageSize	Integer	无	图片规格0:未分类、1:350*350、2:550*412、3:640*960
    '''

    SIZE_CHOICES = {
        (0, '未分类'),
        (1, '350 * 350'),
        (2, '550 * 412'),
        (3, '640 * 960'),
    }

    LOGO_CHOICES = {
        (0, '有水印logo'),
        (1, '无水印logo'),
        (-1, '未知'),
    }

    imageId = models.IntegerField('图片编号', primary_key=True)
    imagetype = models.CharField('图片类型', max_length=50, default='无')
    roomTypeIds = models.CharField('图片关联房型', max_length=100, default='无')
    thumbUrl = models.CharField('缩略图地址', max_length=1000, default='无')
    imageUrl = models.CharField('图片地址', max_length=1000, default='无')
    imageLogo = models.IntegerField('是否带水印', choices=LOGO_CHOICES, default=-1)
    imageSize = models.IntegerField('图片规格', choices=SIZE_CHOICES, default=0)

    hotel = models.ForeignKey(Hotel_info, related_name='images', on_delete=models.CASCADE, verbose_name='酒店')

    sys_create_time = models.DateTimeField('创建时间', auto_now_add=True)
    sys_update_time = models.DateTimeField('更新时间', auto_now=True)
    sys_create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')

    class Meta:
        managed = manageFlag
        verbose_name = '房间图片信息表'
        verbose_name_plural = verbose_name
        db_table = 'room_image_info'


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
