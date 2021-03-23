from django.contrib import admin, messages

# Register your models here.
from hotel_order import models


@admin.register(models.Price_model_info)
class Proce_model_info_admin(admin.ModelAdmin):
    list_display = (
        'price_model_id',
        'name',
        'proportion',
        'level',
    )


@admin.register(models.Order_info)
class Order_info_admin(admin.ModelAdmin):
    list_display = (
        'order_id',
        'hotelid',
        'hotelRemark',
        'status',
        'channel',
        'prices',
        'prices_up',
        'checkInDate',
        'checkOutDate',
        'roomGroups',
        'hotelRemark',
        'status',
        'sys_create_time',
        'sys_update_time',
    )

    list_filter = ('hotelid', 'channel', 'roomGroups')

    # 增加自定义按钮
    actions = ['refresh_status', 'cancelOrder']

    # 更新订单
    def refresh_status(self, request, queryset):
        message_map = {
            True: 0,
            False: 0,
        }

        for order in queryset:
            res = order.queryOrderDetail_status()
            message_map[res] = message_map[res] + 1

        messages.add_message(request, messages.SUCCESS, '成功更新{}条数据'.format(message_map[True]))

    # admin 样式
    refresh_status.short_description = '更新订单状态'
    # icon，参考element-ui icon与https://fontawesome.com
    refresh_status.icon = 'el-icon-goods'
    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    refresh_status.type = 'danger'
    # 给按钮追加自定义的颜色
    refresh_status.style = 'color:blue;'


    # 取消订单
    def cancelOrder(self, request, queryset):
        message_map = {
            True: 0,
            False: 0,
        }

        for order in queryset:
            res = order.cancelOrder('测试取消')
            message_map[res] = message_map[res] + 1

        messages.add_message(request, messages.SUCCESS, '成功取消{}条数据'.format(message_map[True]))

    # admin 样式
    cancelOrder.short_description = '取消订单'
    # icon，参考element-ui icon与https://fontawesome.com
    cancelOrder.icon = 'el-icon-goods'
    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    cancelOrder.type = 'danger'
    # 给按钮追加自定义的颜色
    cancelOrder.style = 'color:red;'