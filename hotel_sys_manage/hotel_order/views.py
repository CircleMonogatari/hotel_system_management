import datetime
import json
from decimal import Decimal

from django.http import HttpResponse
from hotel_api import script
# Create your views here.
from django.shortcuts import render
from django.views import View

from hotel_admin import models as hotel_models
from hotel_admin import baseforms

from hotel_order import models


class Order_create(View):
    page_html = 'hotel_order/submit_data.html'
    api = script.SZ_JL_API()

    CHANNEL_DICT = {
        '深圳捷旅': 'JL',
    }

    def get(self, request):
        data = {}
        list_field = ('hotelid',
                      'channel',
                      'keyId',)
        for d in list_field:
            data[d] = request.GET.get(d, '')

        data_from = baseforms.Hotel_list_from(data)

        return render(request, self.page_html, {'data_from': data_from, 'title': '提交订单'})

    def post(self, request):
        data_from = baseforms.Hotel_list_from(request.POST)
        dic = {
            'msg': '参数无效',
            'status': -1,
        }

        if data_from.is_valid():
            hotelId = data_from.cleaned_data.get('hotelid')
            keyId = data_from.cleaned_data.get('keyId')
            channel = data_from.cleaned_data.get('channel')
            checkInDate = data_from.cleaned_data.get('checkInDate')
            checkOutDate = data_from.cleaned_data.get('checkOutDate')
            hotelRemark = data_from.cleaned_data.get('hotelRemark', '')

            # 酒店产品获取
            rates = hotel_models.RatePlan_info.objects.filter(keyId=keyId, channel=channel, hotel__hotelId=hotelId)
            if rates.exists() is False:
                dic['msg'] = '酒店 key 失效'
                return HttpResponse(json.dumps(dic, ensure_ascii=False), content_type="application/json,charset=utf-8")

            rate = rates[0]

            # 计算入住时间
            date_list = self.creater_date_list(checkInDate, checkOutDate)
            if len(date_list) == 0:
                dic['msg'] = '请重新效验时间'
                return HttpResponse(json.dumps(dic, ensure_ascii=False), content_type="application/json,charset=utf-8")

            # 效验价格
            date_cose_list = rate.get_date_cose(date_list)
            nightlyPrices = ''
            for d in date_list:
                if nightlyPrices == '':
                    nightlyPrices = str(date_cose_list.get(d))
                else:
                    nightlyPrices = nightlyPrices + '|' + str(date_cose_list.get(d))

            # 数据效验
            roomGroups = self.strTojson(data_from.cleaned_data.get('roomGroups', ''))
            if type(roomGroups) != type([]):
                dic['msg'] = '请重新效验roomGroups'
                return HttpResponse(json.dumps(dic, ensure_ascii=False), content_type="application/json,charset=utf-8")

            data = {
                "hotelId": hotelId,
                "keyId": keyId,
                "checkInDate": checkInDate,
                "checkOutDate": checkOutDate,
                "nightlyPrices": nightlyPrices,
                "roomGroups": roomGroups,
            }

            print(data)

            # 订单报价
            jl_res = self.api.JL_queryOrderPrice(data)
            orderPrice = jl_res.get('orderPrice', {})
            bookingMessage = orderPrice.get('bookingMessage', {})
            code = bookingMessage.get('code', -1)
            message = bookingMessage.get('message', '未知错误')
            if code != 0:
                dic['msg'] = 'jl报错：{}'.format(message)
                return HttpResponse(json.dumps(dic, ensure_ascii=False), content_type="application/json,charset=utf-8")

            # 创建订单ID
            # customerOrderCode = self.CHANNEL_DICT.get(channel) + hotelId + self.api.get_timestamp()
            # data['customerOrderCode'] = customerOrderCode
            totalPrice = Decimal(0)
            for i in date_cose_list:

                totalPrice = totalPrice + date_cose_list[i]


            data['totalPrice'] = str(totalPrice)

            # 申请订单
            order_res = self.api.JL_createOrder(data)
            if len(order_res) == 0:
                return HttpResponse(json.dumps(dic, ensure_ascii=False), content_type="application/json,charset=utf-8")

            print(order_res)
            createOrder = order_res.get('createOrder')
            orderCode = createOrder.get('orderCode')
            orderStatus = createOrder.get('orderStatus')

            # 创建订单
            res = models.Order_info.objects.get_or_create(order_id=orderCode, hotelid=hotelId, channel=channel)
            if res[1] is False:
                dic['msg'] = '订单已存在'
                return HttpResponse(json.dumps(dic, ensure_ascii=False),
                                    content_type="application/json,charset=utf-8")
            order_info = res[0]

            order_data = {
                'prices': str(totalPrice),
                'prices_up': str(totalPrice) * 1.15,
                'checkInDate': checkInDate,
                'checkOutDate': checkOutDate,
                'roomGroups': data_from.cleaned_data.get('roomGroups', ''),
                'hotelRemark': hotelRemark,
                'status': order_info.get_status_str(orderStatus)
            }

            for k in order_data:
                setattr(order_data, k, order_data.get(k))

            order_info.save()
            dic = {
                'msg': '订单创建成功',
                'status': 0,
            }

        return HttpResponse(json.dumps(dic, ensure_ascii=False), content_type="application/json,charset=utf-8")
        # return JsonResponse(dic)

    def calc_date(self, InDate, OutDate):
        num = -1
        try:
            a = datetime.datetime.strptime(InDate, '%Y-%m-%d')
            b = datetime.datetime.strptime(OutDate, '%Y-%m-%d')
            num = (b - a).days
        except Exception as e:
            print(e)
        return num

    def creater_date_list(self, InDate, OutDate):
        num = self.calc_date(InDate, OutDate)
        if num < 0:
            return []
        if num == 0:
            return [InDate]

        date_list = []
        day = datetime.datetime.strptime(InDate, '%Y-%m-%d')

        for i in range(num):
            day + datetime.timedelta(days=i)
            date_list.append((day + datetime.timedelta(days=i)).strftime('%Y-%m-%d'))

        return date_list

    def strTojson(self, data):
        res = []
        # TODO: 格式效验
        # group = {
        #     "adults": 2,
        #     "checkInPersions": [
        #         {"lastName": "姓名", "firstName": "test"}
        #     ]
        # }
        try:
            res = json.loads(data)
        except Exception as e:
            print(e)
            res = []
        return res



class Order_cancel(View):
    page_html = 'hotel_order/submit_data.html'
    api = script.SZ_JL_API()

    CHANNEL_DICT = {
        '深圳捷旅': 'JL',
    }

    def get(self, request):
        data = {}


        data_from = baseforms.Order_cannel_from(data)

        return render(request, self.page_html, {'data_from': data_from, 'title': '取消订单'})

    def post(self, request):
        data_from = baseforms.Hotel_list_from(request.POST)
        dic = {
            'msg': '查无此订单',
            'status': -1,
        }

        if data_from.is_valid():
            orderid = data_from.changed_data.get('orderid', '')
            cannel_Remark = data_from.changed_data.get('cannel_Remark', '')
            orders = models.Order_info.objects.filter(order_id=orderid)
            if orders.exists():
                order = orders[0]
                order.cancelOrder(cannel_Remark)

                dic = {
                    'msg': '取消中',
                    'status': 0,
                }
                return HttpResponse(json.dumps(dic, ensure_ascii=False), content_type="application/json,charset=utf-8")
            #
            # orderid
            # hotelid