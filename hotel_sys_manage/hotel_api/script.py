import datetime
import hashlib
import json
import os
import time

import requests


class SZ_JL_API():
    #
    # 名称	编码	类型	示例值	描述
    # 客户编号	appKey	String	SZ28276	捷旅提供
    # 时间戳	timestamp	String	1516816895000	Unix时间戳
    # 数字签名	sign	String	063cae11a00896187f80eecbf922364a	签名方法：md5(md5(secretKey+appKey)+timestamp)md5采用32位小写。
    # 版本	version	String	3.0.1	版本信息，请参考版本说明
    # md5(md5(secretKey+appKey)+timestamp)

    CS_SECRETKEY = '123456'
    CS_APPKEY = 'SZ28276'

    def get_timestamp(slef):
        return str(int(time.time() * 1000))

    def creater_md5(self, data):
        return hashlib.md5(data.encode('UTF-8')).hexdigest()

    def sign(self, timestamp):
        tmp = self.creater_md5((self.CS_SECRETKEY + self.CS_APPKEY))
        return self.creater_md5((tmp + timestamp))

    def get(self, url, payload=None):

        r = requests.get(url, params=payload)
        print(r.url)
        return r

    def post(self, url, data=None, ):
        # post
        r = requests.post(url, data=data)
        print(r.url)
        return r

    def get_head(self, timestamp):
        return {
            "appKey": self.CS_APPKEY,
            "timestamp": timestamp,
            "sign": self.sign(timestamp),
            "version": "3.0.0"
        }

    def creater_payload(self, data):
        return {
            'reqData': json.dumps(data)
        }

    def creater_city_info_list(self, data):
        city_list = []
        for info in data:
            info['channel'] = '深圳捷旅'
            c = models.City_info(**info)
            city_list.append(c)
        models.City_info.objects.bulk_create(city_list)
        pass

    def get_city_list(self):
        url = 'http://58.250.56.211:8081/api/city/queryCity.json'

        timestamp = self.get_timestamp()
        head = self.get_head(timestamp)
        data = {
            "head": head,
            "data": {
                "pageIndex": 1,
                "pageSize": 1000
            }
        }

        # 获取第一次数据
        r = self.get(url, self.creater_payload(data))
        if r.status_code == 200:

            j = json.loads(r.text)
            result = j['result']
            if len(result['hotelGeoList']) > 0:
                self.creater_city_info_list(result['hotelGeoList'])

            count = result['count']
            page_Size = result['pageSize']
            page_max = int(count / page_Size) + 1
            pageIndex = result['pageIndex']

            # 获取剩下的数据
            for i in range(page_max):
                index = i + 1
                if index == pageIndex:
                    continue
                print(index)
                timestamp = self.get_timestamp()
                head = self.get_head(timestamp)
                data = {
                    "head": head,
                    "data": {
                        "pageIndex": index,
                        "pageSize": 1000
                    }
                }
                r = self.get(url, self.creater_payload(data))
                if r.status_code == 200:
                    j = json.loads(r.text)
                    result = j['result']
                    if len(result['hotelGeoList']) > 0:
                        self.creater_city_info_list(result['hotelGeoList'])

    def ger_hotel_list(self, page_index=1):

        url = 'http://58.250.56.211:8081/api/hotel/queryHotelList.json'
        timestamp = self.get_timestamp()
        head = self.get_head(timestamp)

        baseindex = page_index
        data = {
            "head": head,
            "data": {
                "pageIndex": baseindex,
                "pageSize": 1000,
                "countryId": "70007",
            }
        }

        # 获取第一次数据
        r = self.get(url, self.creater_payload(data))
        if r.status_code == 200:

            res = json.loads(r.text)
            result = res['result']
            if len(result['hotels']) > 0:
                self.creater_hotels_info_list(result['hotels'])

            count = result['count']
            page_Size = result['pageSize']
            page_max = int(count / page_Size) + 1
            pageIndex = result['pageIndex']

            # 获取剩下的数据
            for i in range(page_max):
                index = i + 1 + baseindex
                if index == pageIndex:
                    continue

                print(index)
                timestamp = self.get_timestamp()
                head = self.get_head(timestamp)
                data = {
                    "head": head,
                    "data": {
                        "pageIndex": index,
                        "pageSize": 1000,
                        "countryId": "70007",
                    }
                }
                r = self.get(url, self.creater_payload(data))
                if r.status_code == 200:

                    res = json.loads(r.text)
                    print(res)
                    result = res['result']
                    if len(result['hotels']) > 0:
                        self.creater_hotels_info_list(result['hotels'])

    def creater_hotels_info_list(self, data):
        hotels_list = []
        for info in data:
            {'hotelId': 40800, 'countryId': 70007, 'stateId': 70045, 'cityId': 101, 'star': 55,
             'hotelNameCn': '五台山五峰宾馆', 'hotelNameEn': 'Wufeng Hotel', 'addressCn': '忻州 风景名胜区龙泉寺旁',
             'addressEn': 'Longquan Xinzhou scenic area next to the temple', 'phone': '0350-3365800',
             'longitude': '113.562590', 'latitude': '38.996081', 'sellType': 0, 'updateTime': '2019-07-15 16:49:36'}

            city = models.City_info.objects.get(cityId=info['cityId'])
            info['ciyt_info'] = city
            info['star'] = str(info.get('star', 0))
            info['hotelId'] = str(info['hotelId'])
            info['instantConfirmation'] = 0
            print(info)
            c = models.Hotel_info(**info)
            hotels_list.append(c)
        models.Hotel_info.objects.bulk_create(hotels_list)
        pass

    STATIC_INFO_PARAMS_HOTEL = '1'
    STATIC_INFO_PARAMS_ROOM = '2'
    STATIC_INFO_PARAMS_RATE = '3'
    STATIC_INFO_PARAMS_IMAGE = '4'

    def get_hotel_static_info(self, hotelid, params='1,2,3,4'):

        # 不传默认1，多个逗号分隔。1需要酒店静态信息 2需要房型信息 3需要价格类型 4需要酒店图片

        # "data": {"hotelId": 15, "params": "1,2,3,4"}
        url = 'http://58.250.56.211:8081/api/hotel/queryHotelDetail.json'
        timestamp = self.get_timestamp()
        head = self.get_head(timestamp)

        data = {
            "head": head,
            "data": {
                "hotelId": hotelid, "params": params,
            }
        }

        r = self.get(url, self.creater_payload(data))
        if r.status_code == 200:
            return json.loads(r.text)
        return eval("{'code': -1, 'errorMsg': '返回失败'}")

    def get_RatePlan(self, hotelId, checkInDate, checkOutDate):

        url = 'http://58.250.56.211:8081/api/hotel/queryRatePlan.json'
        timestamp = self.get_timestamp()
        head = self.get_head(timestamp)

        '''
        报价查询：输入参数
        名称	    编码	    类型	    是否必填	示例值	描述
        酒店编号	hotelId	Integer	是		无
        入住日期	checkInDate	String	是		yyyy-MM-dd
        离店日期	checkOutDate	String	是		yyyy-MM-dd最大入离日期不能超过90天
        房间信息	roomGroups	RoomGroup[]	否	2成人	常用设置为1个房间2个成人
        数据类型	queryType	Integer	否	0	请求数据类型默认值为1落地,0:全部,1:落地,2.实时
        '''

        {"head":
             {"appKey": "SZ28276", "timestamp": "1516816895000", "sign": "063cae11a00896187f80eecbf922364a",
              "version": "3.0.1"
              },
         "data": {"hotelId": 1, "checkInDate": "2018-01-10", "checkOutDate": "2018-01-20"}
         }

        data = {
            "head": head,
            "data": {
                "hotelId": hotelId,
                "checkInDate": checkInDate,
                "checkOutDate": checkOutDate,
            }
        }

        # 获取第一次数据
        r = self.get(url, self.creater_payload(data))
        if r.status_code == 200:
            return json.loads(r.text)
        return eval("{'code': -1, 'errorMsg': '返回失败'}")

    def get_queryChangedPrice(self, updateTime=None):
        url = 'http://58.250.56.211:8081/api/hotel/queryChangedPrice.json?reqData=xxx'

        timestamp = self.get_timestamp()
        head = self.get_head(timestamp)

        '''
        结果代码	code	Integer	0	0表示请求成功；非0表示存在业务异常。
        结果描述	errorMsg	String		错误描述
        版本	version	String		3.0.0
        结果对象	result	String		不同的请求是不同的对象，错误的请求一般返回为空
        响应码	respId	String		单次响应的唯一编码，业务问题排查请提供编码
        '''

        {"head": {"appKey": "SZ28276", "timestamp": "1516816895000", "sign": "063cae11a00896187f80eecbf922364a",
                  "version": "3.0.0"},
         "data": {"updateTime": "2020-12-28 09:30:29"}}

        {"head": {"appKey": "SZ28276", "timestamp": "1516816895000", "sign": "063cae11a00896187f80eecbf922364a",
                  "version": "3.0.0"}, "data": {"updateTime": "2017-12-28 09:30:29"}}

        data = {
            "head": head,
            "data": {}
        }

        print(data)

        # if updateTime is not None:
        #     data['data'] = {'updateTime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        # 获取第一次数据
        r = self.get(url, self.creater_payload(data))
        if r.status_code == 200:
            return json.loads(r.text)
        return eval("{'code': -1, 'errorMsg': '返回失败'}")

    def get_queryOrderPrice(self, hotelId, keyId, checkInDate, checkOutDate, nightlyPrices, roomGroups):
        url = '	http://58.250.56.211:8081/api/hotel/queryOrderPrice.json'
        timestamp = self.get_timestamp()
        head = self.get_head(timestamp)

        '''
            酒店编号	hotelId	Integer	是		无
            产品编号	keyId	String	是		无
            入住日期	checkInDate	String	是		yyyy-MM-dd
            离店日期	checkOutDate	String	是		yyyy-MM-dd
            每日价格	nightlyPrices	String	是		200.58|120.6|120.8
            房间信息	roomGroups	RoomGroup[]	是	2成人	常用设置为1个房间2个成人
        '''

        {"head": {"appKey": "SZ28276", "timestamp": "1516816895000", "sign": "063cae11a00896187f80eecbf922364a",
                  "version": "3.0.0"},
         "data": {"updateTime": "2020-12-28 09:30:29"}}

        data = {
            "head": head,
            'data': {
                'hotelId': hotelId,
                'keyId': keyId,
                'checkInDate': checkInDate,
                'checkOutDate': checkOutDate,
                'nightlyPrices': nightlyPrices,
                'roomGroups': roomGroups,
            }
        }

        print(data)
        {"head": {"appKey": "SZ28276", "timestamp": "1516816895000", "sign": "063cae11a00896187f80eecbf922364a",
                  "version": "3.0.0"},
         "data": {"hotelId": 171813, "keyId": "SGS8SD#4AA9A#DD#2#A", "checkInDate": "2018-06-21",
                  "checkOutDate": "2018-06-23", "nightlyPrices": "150|150", "roomGroups": [{"adults": 2}]}}

        {'code': 0, 'errorMsg': '', 'result': {'orderPrice': {'hotelRatePlans': [{'hotelId': 1, 'rooms': [
            {'roomTypeId': '3191289', 'ratePlans': [
                {'keyId': 'S#D6GGG4#DSHS28H#HHHGGHA#A', 'keyName': '商务楼豪华大床房', 'supplierId': 367774, 'bedName': '1张大床',
                 'maxOccupancy': 2, 'currency': 'CNY', 'rateTypeId': '9997790', 'paymentType': 0, 'breakfast': 0,
                 'bookingRuleId': '##W#7#W#9Q#Q#PW#WOEORO4O5OTO7#QQAQQ#RQAQQ', 'refundRuleId': '1', 'nightlyRates': [
                    {'formulaType': 1, 'date': '2021-03-14', 'cose': 213.0, 'status': 3, 'currentAlloment': 0,
                     'ifInvoice': 2}], 'market': 'ALL|-1'}]}], 'bookingRules': [
            {'bookingRuleId': '##W#7#W#9Q#Q#PW#WOEORO4O5OTO7#QQAQQ#RQAQQ', 'minAmount': 1, 'maxAmount': 7, 'minDays': 1,
             'maxDays': 90, 'minAdvHours': 0, 'maxAdvHours': -1, 'weekSet': '1,2,3,4,5,6,7', 'startTime': '00:00',
             'endTime': '30:00', 'bookingNotices': ''}], 'refundRules': []}],
                                                              'bookingMessage': {'code': 5, 'message': '满房'}}},
         'respId': '6d8e0ef2-25c4-418e-8439-659d0ab0e3aa'}

        r = self.post(url, data=self.creater_payload(data))
        if r.status_code == 200:
            return json.loads(r.text)
        return eval("{'code': -1, 'errorMsg': '返回失败'}")


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotel_sys_manage.settings")

    import django

    django.setup()
    from hotel_admin import models

    print('request start')
    a = SZ_JL_API()

    # 获取城市
    # a.get_city_list()

    # 获取酒店数据
    # a.ger_hotel_list(2)

    # 获取静态数据 参数 酒店id
    # a.get_hotel_static_info('1')

    # 获取报价
    # print(a.get_RatePlan('1', '2021-3-10', '2021-5-1'))

    # 获取变价
    print(a.get_queryChangedPrice())

    # 订单报价接口
    hotelId = '1'
    keyId = 'S#D6GGG4#DSHS28H#HHHGGHA#A'
    checkInDate = '2021-4-14'
    checkOutDate = '2021-4-15'
    nightlyPrices = '213.0'
    roomGroups = [
        {
            'adults': 2,
            # children
            # childAges
        }
    ]


    # 订单报价
    print(a.get_queryOrderPrice(hotelId, keyId, checkInDate, checkOutDate, nightlyPrices, roomGroups))
