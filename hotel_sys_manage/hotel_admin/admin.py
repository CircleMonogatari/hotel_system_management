from django.contrib import admin
from django.contrib import messages

from hotel_admin import models
from hotel_api import script

# Register your models here.

admin.site.site_header = '坤齐酒店管理系统'  # 设置header
admin.site.site_title = '坤齐酒店管理系统'  # 设置title

API = script.SZ_JL_API()


# class Record_Creater_Action(object):
#     record_model = None
#     record_model_field = 'obj'
#
#     def record_create(self, request, queryset):
#         if self.record_model is None:
#             return
#         for q in queryset:
#             data = {
#                 self.record_model_field: q,
#             }
#
#             self.record_model.objects.create(**data)
#
#         return HttpResponse('ok')
#
#     record_create.short_description = '生成报告记录'


@admin.register(models.City_info)
class City_info_admin(admin.ModelAdmin):
    list_display = (
        'cityId',
        'cityCn',
        'cityEn',

        'countryId',
        'countryCn',
        'countryEn',
        'stateId',
        'stateCn',
        'stateEn',

        'is_effective',

        'sys_create_time',
        'sys_update_time',
        'sys_create_user',
    )
    list_filter = (
        'countryCn',
        'countryEn',
    )


@admin.register(models.Hotel_info)
class Hotel_info_admin(admin.ModelAdmin):
    list_display = (

        'hotelId',
        'countryId',
        'stateId',
        'cityId',
        'ciyt_info',
        'star',
        'hotelNameCn',
        'hotelNameEn',
        'addressCn',
        'addressEn',
        'phone',
        'longitude',
        'latitude',
        'instantConfirmation',
        'sellType',
        'updateTime',
        'detail',

        'themeType',
        'area',
        'businessCircle',
        'fax',
        'email',
        'postCode',
        'checkPolicy',
        'childrenPolicy',
        'petPolicy',
        'establishmentDate',
        'renovationDate',
        'hotelGroup',
        'hotelBrand',
        'facilities',
        'cardType',
        'minPrice',
        'introduceCn',
        'introduceEn',

        'sys_create_time',
        'sys_update_time',
        'sys_create_user',
    )

    # list_filter = ('hotelNameCn', 'ciyt_info__cityCn',)
    search_fields = ('hotelNameCn', 'ciyt_info__cityCn',)

    # record_model_field = 'api'
    # record_model = models.Api_Record_info
    # actions = ['record_create']

    # 增加自定义按钮
    actions = ['refresh_hotel_info', ]

    # 更新静态信息
    def refresh_hotel_info(self, request, queryset):

        message_map = {
            True: 0,
            False: 0,
            'plus': 0,

        }

        for hotel in queryset:
            data = API.get_hotel_static_info(str(hotel.pk), '1,2,3,4')
            if data.get('code', -1) == 0:
                hotelDetailList = data.get('result', {}).get('hotelDetailList', [])
                if len(hotelDetailList) > 0:
                    # 酒店信息
                    hotelInfo = hotelDetailList[0].get('hotelInfo', {})
                    roomTypeList = hotelDetailList[0].get('roomTypeList', [])
                    rateTypeList = hotelDetailList[0].get('rateTypeList', [])
                    imageList = hotelDetailList[0].get('imageList', [])

                    # 静态信息
                    res = hotel.set_puls_info(hotelInfo)

                    # 房间信息 价格类型 静态图片
                    if hotel.refresh_puls_static_info(roomTypeList, rateTypeList, imageList) is False:
                        message_map['plus'] = message_map['plus'] + 1

                    message_map[res] = message_map[res] + 1
                else:
                    print('Error :refresh_hotel_info--{}'.format(hotelInfo))
                    message_map[False] = message_map[False] + 1

        messages.add_message(request, messages.SUCCESS, '成功写入{}条数据'.format(message_map[True]))
        messages.add_message(request, messages.ERROR, '失败{}条'.format(message_map[False]))
        if message_map['plus'] > 0:
            messages.add_message(request, messages.ERROR, '扩展信息失败{}条'.format(message_map['plus']))

    # admin 样式
    refresh_hotel_info.short_description = '更新酒店信息'
    # icon，参考element-ui icon与https://fontawesome.com
    refresh_hotel_info.icon = 'fas fa-audio-description'
    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    refresh_hotel_info.type = 'danger'
    # 给按钮追加自定义的颜色
    refresh_hotel_info.style = 'color:black;'


    # 更新产品信息
    def refresh_hotel_rateplan_info(self, request, queryset):
        message_map = {
            True: 0,
            False: 0,
            'plus': 0,

        }
        for hotel in queryset:

            pass

        messages.add_message(request, messages.SUCCESS, '成功写入{}条数据'.format(message_map[True]))
        messages.add_message(request, messages.ERROR, '失败{}条'.format(message_map[False]))
        if message_map['plus'] > 0:
            messages.add_message(request, messages.ERROR, '扩展信息失败{}条'.format(message_map['plus']))
        pass
    # admin 样式
    refresh_hotel_rateplan_info.short_description = '更新酒店产品'
    # icon，参考element-ui icon与https://fontawesome.com
    refresh_hotel_rateplan_info.icon = 'el-icon-goods'
    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    refresh_hotel_rateplan_info.type = 'danger'
    # 给按钮追加自定义的颜色
    refresh_hotel_rateplan_info.style = 'color:blue;'



@admin.register(models.Price_model_info)
class Proce_model_info_admin(admin.ModelAdmin):
    list_display = (
        'price_model_id',
        'name',
        'proportion',
        'level',
    )


@admin.register(models.Room_type_info)
class Room_type_info_admin(admin.ModelAdmin):
    list_display = (
        'roomTypeId',
        'roomTypeCn',
        'roomTypeEn',
        'roomTypeEn',
        'basisroomId',
        'basisroomCn',
        'maximize',
        'acreage',
        'bedWidth',
        'floorDistribute',
        'facilities',
        'extraBedtState',
        'bedCount',
        'sys_create_time',
        'sys_update_time',
        'sys_create_user',
        'hotel',
    )

    list_filter = ('basisroomCn',)


@admin.register(models.Rate_type_info)
class rate_type_info_admin(admin.ModelAdmin):
    list_display = (
        'rateTypeId',
        'rateTypeCn',
        'rateTypeEn',
        'hotel',
        'sys_create_time',
        'sys_update_time',
        'sys_create_user',
    )

    search_fields = ('rateTypeCn',)


@admin.register(models.Room_image_info)
class room_image_info_admin(admin.ModelAdmin):
    list_display = (
        'imageId',
        'imagetype',
        'roomTypeIds',
        'thumbUrl',
        'image_data',
        'imageLogo',
        'imageSize',
        'hotel',
        'sys_create_time',
        'sys_update_time',
        'sys_create_user',
    )

    # list_filter = ('basisroomCn',)


@admin.register(models.Order_info)
class Order_info_admin(admin.ModelAdmin):
    list_display = (
        'order_id',
        'room_type',
        'hotel',
        'channel',
        'price',
        'custom_proce',
        'sys_create_time',
        'sys_update_time',
        'sys_create_user',
    )

    list_filter = ('room_type', 'room_type', 'channel')
