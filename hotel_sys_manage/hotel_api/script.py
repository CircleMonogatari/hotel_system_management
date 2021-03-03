import hashlib
import json
import os
import time

import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotel_sys_manage.settings")

import django

django.setup()

from hotel_admin import models


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

        return r

    def post(self, url, data, body):
        # post
        r = requests.post('http://httpbin.org/post', data={'key': 'value'})

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
            print(info)
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

        pass


if __name__ == '__main__':
    print('request start')
    a = SZ_JL_API()
    a.get_city_list()
