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
    id = models.BigAutoField('编号', primary_key=True)
    channel = models.CharField('渠道', max_length=50, default='未知')

    cityId = models.CharField('城市编号', max_length=50, )
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

    id = models.BigAutoField('编号', primary_key=True)
    channel = models.CharField('渠道', max_length=50, default='未知')

    hotelId = models.IntegerField('酒店编号', )
    countryId = models.IntegerField('国家编号', )
    stateId = models.IntegerField('省份编号', )
    cityId = models.IntegerField('城市编号', )
    ciyt_info = models.ForeignKey(City_info, null=True, on_delete=models.SET_NULL)

    star = models.CharField('酒店星级', max_length=20, default=0)

    hotelNameCn = models.CharField('酒店中文名', max_length=500, default='无')
    hotelNameEn = models.CharField('酒店英文名', max_length=1000, default='无')
    addressCn = models.CharField('中文地址', max_length=500, default='无')
    addressEn = models.CharField('英文地址', max_length=1000, default='无')
    phone = models.CharField('酒店总机', max_length=100, default='无')
    longitude = models.CharField('经度', max_length=20, default='无')
    latitude = models.CharField('纬度', max_length=20, default='无')
    instantConfirmation = models.IntegerField('是否即时确认', default=0)
    sellType = models.IntegerField('是否热销酒店', default=0)
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

    def refresh_puls_static_info(self, roomTypeList, rateTypeList, imageList):
        res = False
        res = False and self.creater_rooms(roomTypeList)
        res = False and self.creater_rateTypeList(rateTypeList)
        res = False and self.creater_imageList(imageList)

        return res

    def set_puls_info(self, data):
        if len(data) == 0:
            return False
        try:
            quset = Hotel_info.objects.filter(pk=self.pk)
            data['channel'] = '深圳捷旅'
            data['hotelId'] = str(data.pop('hotelId'))
            quset.update(**data)
        except Exception as exc:
            print(exc)
            return False
        return True

    def creater_rooms(self, rooms):
        try:
            for room in rooms:
                roomTypeId = room.get('roomTypeId', '')
                if roomTypeId == '':
                    continue
                room['hotel'] = self
                room['channel'] = '深圳捷旅'
                res = Room_type_info.objects.get_or_create(roomTypeId=roomTypeId, hotel=self)

                if res[1] is False:
                    print('数据覆盖 原{}, 改{}'.format(res[0], room))
                r = res[0]
                for k in room:
                    setattr(r, k, room[k])
                r.save()

        except Exception as exc:
            print(exc)
            return False
        return True

    def creater_rateTypeList(self, rateTypeList):
        try:
            for rate in rateTypeList:
                # 数据转换 字段数据不统一
                rate['rateTypeId'] = rate.pop('ratetypeId', '')
                rate['rateTypeCn'] = rate.pop('ratetypeCn', '')
                rate['rateTypeEn'] = rate.pop('ratetypeEn', '')

                rateTypeId = rate.get('rateTypeId', '')
                if rateTypeId == '':
                    continue
                rate['hotel'] = self
                rate['channel'] = '深圳捷旅'
                res = Rate_type_info.objects.get_or_create(rateTypeId=rateTypeId, hotel=self)

                if res[1] is False:
                    print('数据覆盖 原{}, 改{}'.format(res[0], rate))
                r = res[0]
                for k in rate:
                    setattr(r, k, rate[k])
                r.save()

        except Exception as exc:
            print(exc)
            return False
        return True

    def creater_imageList(self, imageList):

        try:
            for info in imageList:

                '''
                channel
                imageId
                imagetype
                roomTypeIds
                thumbUrl
                imageUrl
                imageLogo
                imageSize
                '''

                imageId = info.pop('imageId', '')
                if imageId == '':
                    continue
                info['hotel'] = self
                info['imagetype'] = info.pop('type', 0)
                # info['roomTypeIds'] = info.pop('roomTypeIds', '')
                info['thumbUrl'] = info.pop('thumbUrl', '')
                info['imageUrl'] = info.pop('imageUrl', '')
                info['imageLogo'] = info.pop('imageLogo', 0)
                info['imageSize'] = info.pop('imageSize', 0)

                res = Room_image_info.objects.get_or_create(imageId=imageId, hotel=self)

                if res[1] is False:
                    print('数据覆盖 原{}, 改{}'.format(res[0], info))
                r = res[0]
                for k in info:
                    setattr(r, k, info[k])
                r.save()

        except Exception as exc:
            print(exc)
            return False
        return True


class Room_type_info(models.Model):
    id = models.BigAutoField('编号', primary_key=True)
    channel = models.CharField('渠道', max_length=50, default='未知')

    roomTypeId = models.CharField('房型编号', max_length=50, )  # 无
    roomTypeCn = models.CharField('客房中文名称', max_length=50, default='无')  # 无
    roomTypeEn = models.CharField('客房英文名称', max_length=100, default='无')  # 无
    basisroomId = models.IntegerField('基础房型ID', default=-1)  # 278954	基础房型仅供参考，无物理房型的，返回-1
    basisroomCn = models.CharField('基础房型中文名', max_length=50, default='无')  # 城景行政豪华房	基础房型仅供参考，无物理房型的，返回-1
    maximize = models.IntegerField('最大入住人数', default=-1)  # 无
    acreage = models.CharField('房间面积', max_length=50, default='无')  # 无
    bedWidth = models.CharField('床大小', max_length=50, default='无')  # 无
    floorDistribute = models.CharField('楼层', max_length=50, default='无')  # 无
    facilities = models.CharField('房型设施', max_length=50, default='无')  # 无
    extraBedtState = models.CharField('是否允许加床', max_length=50, default='无')  # 无
    bedCount = models.IntegerField('加床数量', default=-1)  # 无

    bedType = models.CharField('类型', max_length=50, default='')
    bedName = models.CharField('名称', max_length=100, default='')

    sys_create_time = models.DateTimeField('创建时间', auto_now_add=True)
    sys_update_time = models.DateTimeField('更新时间', auto_now=True)
    sys_create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')

    hotel = models.ForeignKey(Hotel_info, related_name='rooms', on_delete=models.SET_NULL, null=True, verbose_name='酒店')

    class Meta:
        managed = manageFlag
        verbose_name = '房间信息表'
        verbose_name_plural = verbose_name
        db_table = 'Room_type_info'


class Rate_type_info(models.Model):
    '''
    价格类型编号	rateTypeId	Integer	无
    价格类型中文名	rateTypeCn	String	无
    价格类型英文名	rateTypeEn	String  无
    '''
    id = models.BigAutoField('编号', primary_key=True)
    channel = models.CharField('渠道', max_length=50, default='未知')

    rateTypeId = models.CharField('价格类型编号', max_length=100, )
    rateTypeCn = models.CharField('价格类型中文名', max_length=100)
    rateTypeEn = models.CharField('价格类型英文名', max_length=500)

    hotel = models.ForeignKey(Hotel_info, related_name='rates', on_delete=models.SET_NULL, null=True, verbose_name='酒店')

    sys_create_time = models.DateTimeField('创建时间', auto_now_add=True)
    sys_update_time = models.DateTimeField('更新时间', auto_now=True)
    sys_create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')

    class Meta:
        managed = manageFlag
        verbose_name = '价格类型'
        verbose_name_plural = verbose_name
        db_table = 'rate_type_info'


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

    id = models.BigAutoField('编号', primary_key=True)
    channel = models.CharField('渠道', max_length=50, default='未知')

    imageId = models.CharField('图片编号', max_length=50, )
    imagetype = models.CharField('图片类型', max_length=50, default='无')
    roomTypeIds = models.CharField('图片关联房型', max_length=100, default='无')
    thumbUrl = models.CharField('缩略图地址', max_length=1000, default='无')
    imageUrl = models.CharField('图片地址', max_length=1000, default='无')
    imageLogo = models.IntegerField('是否带水印', choices=LOGO_CHOICES, default=-1)
    imageSize = models.IntegerField('图片规格', choices=SIZE_CHOICES, default=0)

    hotel = models.ForeignKey(Hotel_info, related_name='images', on_delete=models.SET_NULL, null=True,
                              verbose_name='酒店')

    sys_create_time = models.DateTimeField('创建时间', auto_now_add=True)
    sys_update_time = models.DateTimeField('更新时间', auto_now=True)
    sys_create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')

    class Meta:
        managed = manageFlag
        verbose_name = '房间图片信息表'
        verbose_name_plural = verbose_name
        db_table = 'room_image_info'


class RatePlan_info(models.Model):
    '''
     价格类型编号	rateTypeId	Integer	无
     价格类型中文名	rateTypeCn	String	无
     价格类型英文名	rateTypeEn	String  无
     '''
    id = models.BigAutoField('编号', primary_key=True)
    channel = models.CharField('渠道', max_length=50, default='未知')

    keyId = models.CharField('产品编号', max_length=50, default='')  # 无	唯一产品编号
    supplierId = models.IntegerField('供应商ID', default=0)  # 无	区分价格
    keyName = models.CharField('房型名称', max_length=50, default='')  # 标准房
    bedName = models.CharField('床型名称', max_length=50, default='')  # 大床
    maxOccupancy = models.IntegerField('最大入住人数', default=0)  # 2	房间最大入住人数
    currency = models.CharField('币种', max_length=50, default='')  # CNY
    rateTypeId = models.CharField('价格类型编号', max_length=50, default='')  # 无
    paymentType = models.IntegerField('付款类型', default=0)  # 无	0预付
    breakfast = models.IntegerField('早餐', default=0)  # 无	0:无早、1:一份、2:两份...99:床位早、-1:含早(不确定早餐份数)
    ifInvoice = models.IntegerField('是否开票', default=0)  # 无	1:可开票 2：不可开票

    bookingRuleId = models.CharField('预订条款编号', max_length=50, default='')  # 无
    refundRuleId = models.CharField('取消条款编号', max_length=50, default='')  # 无	为空默认是为1不可退。
    market = models.CharField('适用市场', max_length=50, default='')  # CHN,HKG|	适用市场,适用市场|不适用市场,不适用市场分隔符前或后为-1，表示不限制

    # nightlyRates = models.NightlyRate('间夜价格数组', )  # []	无  外键
    # promotion_list = models.Promotion('礼包信息', )  # []	无

    hotel = models.ForeignKey(Hotel_info, related_name='rateplans', on_delete=models.SET_NULL, null=True,
                              verbose_name='酒店')

    sys_create_time = models.DateTimeField('创建时间', auto_now_add=True)
    sys_update_time = models.DateTimeField('更新时间', auto_now=True)
    sys_create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')

    class Meta:
        managed = manageFlag
        verbose_name = '产品信息'
        verbose_name_plural = verbose_name
        db_table = 'rateplan_info'


class Hotel_NightlyRate_info(models.Model):
    id = models.BigAutoField('编号', primary_key=True)
    channel = models.CharField('渠道', max_length=50, default='未知')

    formulaTypen = models.CharField('配额类型', max_length=50, default='')  # String	如：配额房、包房等,字段对应的code含义只对深捷旅有意义
    date = models.CharField('日期', default='', max_length=20)  # String	无	yyyy-MM-dd
    cose = models.DecimalField('价格', decimal_places=4, max_digits=10, default=0.0)  # Double	无
    status = models.IntegerField('房态', default=0)  # Integer	无	1:保留房、2:待查、3:满房、4:限时确认
    currentAlloment = models.IntegerField('库存', default=0)  # Integer	无	库存数量
    breakfast = models.IntegerField('早餐', default=0)  # Integer	无	此处日历早餐,需要优先获取、无节点则拿上一级节点早餐
    bookingRuleId = models.CharField('预订条款编号', max_length=20, default='')  # String	无	优先获取、无节点或无条款则拿上一级节点条款
    refundRuleId = models.CharField('取消条款编号', max_length=20, default='')  # String	无	优先获取、无节点或无条款则拿上一级节点条款

    hotel = models.ForeignKey(Hotel_info, on_delete=models.SET_NULL, null=True, verbose_name='酒店')
    Rateplan = models.ForeignKey(RatePlan_info, related_name='nightlyRates', on_delete=models.SET_NULL, null=True,
                                 verbose_name='酒店产品')

    sys_create_time = models.DateTimeField('创建时间', auto_now_add=True)
    sys_update_time = models.DateTimeField('更新时间', auto_now=True)
    sys_create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')

    class Meta:
        managed = manageFlag
        verbose_name = '夜间数据'
        verbose_name_plural = verbose_name
        db_table = 'hotel_nightlyrate_info'


class Hotel_BookingRule_info(models.Model):
    id = models.BigAutoField('编号', primary_key=True)
    channel = models.CharField('渠道', max_length=50, default='未知')

    bookingRuleId = models.CharField('预订条款编号', max_length=100)  # String	无
    startDate = models.CharField('开始日期', max_length=100)  # String	无	报价生效时间yyyy-MM-dd HH:mm:ss 为空表示无限制
    endDate = models.CharField('结束日期', max_length=100)  # String	无	报价结束时间yyyy-MM-dd HH:mm:ss 为空表示无限制
    minAmount = models.IntegerField('预订最少数量', default=1)  # Integer	1	最少预定房间数量
    maxAmount = models.IntegerField('预订最多数量', default=7)  # Integer	7	最大预定房间数量
    minDays = models.IntegerField('最少入住天数', default=1)  # Integer	1	最少入住天数
    maxDays = models.IntegerField('最多入住天数', default=30)  # Integer	30	最多入住天数
    minAdvHours = models.IntegerField('最少提前预订时间', default=0)  # Integer	0	最少提前预订时间（以用户选择的入住日期的23:59:59计算）
    maxAdvHours = models.IntegerField('最大提前预订时间', default=-1)  # Integer	-1	最大提前预定时间（以用户选择的入住日期的23:59:59计算）-1表示为无限制
    weekSet = models.CharField('有效星期', max_length=100)  # String	1,2,3,4,5,6,7	有效星期。7表示星期日，1表示星期一，剩余的以此类推。当天不在星期范围内则无法下单
    startTime = models.CharField('每日开始销售时间', max_length=100)  # String	HH:mm	销售起始小时数，默认值00:00
    endTime = models.CharField('每日结束销售时间', max_length=100)  # String	HH:mm	销售结束小时，默认值30:00，代表第二天早上6点前还可以进行预定
    bookingNotices = models.CharField('预订说明', max_length=2000)  # String	无	预定说明，没有强校验。请注意合理使用。

    hotel = models.ForeignKey(Hotel_info, related_name='bookingrules', on_delete=models.SET_NULL, null=True,
                              verbose_name='酒店')

    sys_create_time = models.DateTimeField('创建时间', auto_now_add=True)
    sys_update_time = models.DateTimeField('更新时间', auto_now=True)
    sys_create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')

    class Meta:
        managed = manageFlag
        verbose_name = '预订条款信息'
        verbose_name_plural = verbose_name
        db_table = 'hotel_bookingrule_info'


class Hotel_RefundRule_info(models.Model):
    id = models.BigAutoField('编号', primary_key=True)
    channel = models.CharField('渠道', max_length=50, default='未知')

    hotel = models.ForeignKey(Hotel_info, related_name='refundrules', on_delete=models.SET_NULL, null=True,
                              verbose_name='酒店')

    refundRuleId = models.CharField('取消条款编号', max_length=50, )  # 无
    refundRuleType = models.IntegerField('取消条款规则', default=1)  # 无	当返回数据为空时，默认不可取消;1:不可退、2:限时取消
    refundRuleHours = models.IntegerField('入住前n小时', default=30)  # 无	30
    deductType = models.IntegerField('取消客人罚金', default=1)  # 无	1扣全额、0扣首晚房费

    sys_create_time = models.DateTimeField('创建时间', auto_now_add=True)
    sys_update_time = models.DateTimeField('更新时间', auto_now=True)
    sys_create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')

    class Meta:
        managed = manageFlag
        verbose_name = '取消条款信息'
        verbose_name_plural = verbose_name
        db_table = 'hotel_refundrule_info'


class Hotel_Promotion_info(models.Model):
    id = models.BigAutoField('编号', primary_key=True)
    channel = models.CharField('渠道', max_length=50, default='未知')

    startDate = models.CharField('礼包开始时间', max_length=200, default='')  # String	yyyy-MM-dd	在店时间生效
    endDate = models.CharField('礼包结束时间', max_length=200, default='')  # String	yyyy-MM-dd
    description = models.CharField('礼包描述', max_length=200, default='')  # String	无	礼包描述

    RatePlan = models.ForeignKey(RatePlan_info, related_name='promotions', on_delete=models.SET_NULL, null=True,
                                 verbose_name='酒店产品')

    sys_create_time = models.DateTimeField('创建时间', auto_now_add=True)
    sys_update_time = models.DateTimeField('更新时间', auto_now=True)
    sys_create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')

    class Meta:
        managed = manageFlag
        verbose_name = '礼包信息'
        verbose_name_plural = verbose_name
        db_table = 'hotel_promotion_info'


class My____________________(object):
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
