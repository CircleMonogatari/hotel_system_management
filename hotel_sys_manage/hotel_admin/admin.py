from django.contrib import admin
from django.contrib import messages

from hotel_admin import models
from hotel_api import script

# Register your models here.

admin.site.site_header = '测试系统'  # 设置header
admin.site.site_title = '测试系统'  # 设置title

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
    actions = ['refresh_hotel_info', 'refresh_room_info', 'refresh_rate_info', 'refresh_image_info']

    def refresh_hotel_info(self, request, queryset):
        info_list = []

        for hotel in queryset:
            data = API.get_hotel_static_info(str(hotel.pk), '1')
            info_list.append(data)
            print(hotel)
            print(data)

    def refresh_room_info(self, request, queryset):
        info_list = []

        for hotel in queryset:
            data = API.get_hotel_static_info(hotel.pk, '2')
            info_list.append(data)

            messages.INFO(request, '请求成功{}'.format(data))

    def refresh_rate_info(self, request, queryset):
        info_list = []

        for hotel in queryset:
            data = API.get_hotel_static_info(hotel.pk, '3')
            info_list.append(data)

            messages.INFO(request, '请求成功{}'.format(data))

    def refresh_image_info(self, request, queryset):
        info_list = []

        for hotel in queryset:
            data = API.get_hotel_static_info(hotel.pk, '4')
            info_list.append(data)

            messages.INFO(request, '请求成功{}'.format(data))

    # admin 样式
    refresh_hotel_info.short_description = '更新酒店信息'
    # icon，参考element-ui icon与https://fontawesome.com
    refresh_hotel_info.icon = 'fas fa-audio-description'
    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    refresh_hotel_info.type = 'danger'
    # 给按钮追加自定义的颜色
    refresh_hotel_info.style = 'color:black;'

    refresh_room_info.short_description = '更新酒店房型'
    refresh_rate_info.short_description = '更新价格'
    refresh_image_info.short_description = '刷新图片'


@admin.register(models.Price_model_info)
class Proce_model_info_admin(admin.ModelAdmin):
    list_display = (
        'price_model_id',
        'name',
        'proportion',
        'level',
    )



@admin.register(models.Room_info)
class Room_info_admin(admin.ModelAdmin):
    list_display = (
        'roomTypeId',
        'roomTypeCn',
        'roomTypeEn',
        'roomTypeEn',
        'basisroomid',
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

@admin.register(models.Rate_info)
class rate_info_admin(admin.ModelAdmin):
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
        'imageUrl',
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
