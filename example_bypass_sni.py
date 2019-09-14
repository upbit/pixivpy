# -*- coding:utf-8 -*-
"""
@author: Perol_Notsf
简单原理实现示例：
import requests
from requests_toolbelt.adapters import host_header_ssl
url = "https://app-api.pixiv.net/v1/walkthrough/force-like-illusts"
s = requests.Session()
s.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
response=s.get('https://210.140.131.219/v1/walkthrough/force-like-illusts', headers={'host': 'app-api.pixiv.net'})
print(response.json())
"""
from pixivpy3.bapi import ByPassSniApi

api = ByPassSniApi()
api.login("username", "password")
#自行指定pixiv的ip地址
#api.set_api_ipadress(ipadress="https://210.140.131.220")

# get origin url
json_result = api.illust_detail(59580629)
illust = json_result.illust
print(">>> origin url: %s" % illust.image_urls['large'])

# get ranking: 1-30
# mode: [day, week, month, day_male, day_female, week_original, week_rookie, day_manga]
json_result = api.illust_ranking('day')
for illust in json_result.illusts:
    print(" p1 [%s] %s" % (illust.title, illust.image_urls.medium))

# next page: 31-60
next_qs = api.parse_qs(json_result.next_url)
json_result = api.illust_ranking(**next_qs)
for illust in json_result.illusts:
    print(" p2 [%s] %s" % (illust.title, illust.image_urls.medium))