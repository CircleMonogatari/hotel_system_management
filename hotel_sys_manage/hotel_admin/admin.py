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


@admin.register(models.Hotel_info)
class Hotel_info_admin(admin.ModelAdmin):
    list_display = (
        'hotel_id',
        'city',
        'address',
        'name',

        'sys_create_time',
        'sys_update_time',
        'sys_create_user',
    )

    list_filter = ('city', 'name',)
    search_fields = ('city', 'name',)
    # list_filter = ('project', 'sort',)
    # record_model_field = 'api'
    # record_model = models.Api_Record_info
    # actions = ['record_create']
