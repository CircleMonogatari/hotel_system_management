# -- coding: utf-8 --
from django import forms


class Hotel_list_from(forms.Form):
    hotelid = forms.CharField(label='酒店id')
    channel = forms.CharField(label='渠道')
    keyId = forms.CharField(label='产品ID')
    checkInDate = forms.CharField(label='入住时间')
    checkOutDate = forms.CharField(label='离店时间')
    roomGroups = forms.CharField(label='入住人信息',
                                 help_text='json: [{"adults": 2, "checkInPersions": [{"lastName": "姓名", "firstName": "test"}]}]', )
    hotelRemark = forms.CharField(label='备注')


class Order_cannel_from(forms.Form):
    orderid = forms.CharField(label='订单id')
    remark = forms.CharField(label='取消原因')
