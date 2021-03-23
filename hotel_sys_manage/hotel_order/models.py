from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from hotel_api import script

manageFlag = True


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
    order_id = models.CharField(primary_key=True, max_length=200, )
    hotelid = models.CharField('酒店ID', max_length=50, )
    channel = models.CharField('渠道', max_length=100, )

    prices = models.CharField('酒店报价', max_length=100)
    prices_up = models.CharField('实际价格', max_length=100)

    checkInDate = models.CharField('日期', default='', max_length=20)  # String	无	yyyy-MM-dd
    checkOutDate = models.CharField('日期', default='', max_length=20)  # String	无	yyyy-MM-dd
    roomGroups = models.TextField('入住信息', )
    hotelRemark = models.TextField('酒店备注', default='')  # String	无	yyyy-MM-dd

    status = models.CharField('订单状态', max_length=30, default='待确认')

    sys_create_time = models.DateTimeField('创建时间', auto_now_add=True)
    sys_update_time = models.DateTimeField('更新时间', auto_now=True)
    sys_create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')

    class Meta:
        managed = manageFlag
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name
        db_table = 'order_info'

    JL_STATUS = {
        1: '待确认',
        2: '已确认',
        3: '已拒单',
        4: '已取消'
    }

    def get_status_str(self, code):
        if self.channel == '深圳捷旅':
            return self.JL_STATUS.get(int(code), '未知状态')

    def cancelOrder(self, cancelRemark):
        if self.channel == '深圳捷旅':
            api = script.SZ_JL_API()
            data = api.JL_cancelOrder(self.order_id, cancelRemark)
            successs = data.get('successs', -1)

            if successs == 0:
                self.status = '已取消'
                self.save()
                return True
            else:
                print(data)

            return False

    def queryOrderDetail_status(self):
        if self.channel == '深圳捷旅':
            api = script.SZ_JL_API()
            data = api.JL_queryOrderDetail(self.order_id)

            # 这里仅只进行订单的状态更新， 其他不做操作。
            orderDetailList = data.get('orderDetailList', {})
            if len(orderDetailList) > 1:
                print(orderDetailList)
            for orderDetail in orderDetailList:
                orderCode = orderDetail.get('orderCode', '')
                hotelId = orderDetail.get('hotelId', '')
                orderStatus = orderDetail.get('orderStatus', '')

                if (orderCode == self.order_id) and (str(hotelId) == self.hotelid):
                    self.status = self.get_status_str(orderStatus)
                    self.save()

                    return True

            return False
