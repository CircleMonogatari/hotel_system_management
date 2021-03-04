from django.contrib import admin

from hotel_admin import models

# Register your models here.

admin.site.site_header = '测试系统'  # 设置header
admin.site.site_title = '测试系统'  # 设置title


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
        'sys_create_time',
        'sys_update_time',
        'sys_create_user',
    )

    list_filter = ('hotelNameCn', 'ciyt_info__cityCn',)
    # search_fields = ('city', 'name',)
    # list_filter = ('project', 'sort',)
    # record_model_field = 'api'
    # record_model = models.Api_Record_info
    # actions = ['record_create']


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
        'room_id',
        'room_type',
        'hotel',
        'price',
        'custom_proce',

        'sys_create_time',
        'sys_update_time',
        'sys_create_user',
    )

    list_filter = ('room_type',)


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
