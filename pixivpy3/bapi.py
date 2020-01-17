# -*- coding:utf-8 -*-

import requests
from requests_toolbelt.adapters import host_header_ssl
import re
from .aapi import AppPixivAPI


class ByPassSniApi(AppPixivAPI):

    def __init__(self, **requests_kwargs):
        """initialize requests kwargs if need be"""
        super(AppPixivAPI, self).__init__(**requests_kwargs)
        session = requests.Session()
        session.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
        self.requests = session

    def require_appapi_hosts(self, hostname="app-api.pixiv.net"):
        """
        请求真实的ip地址
        """
        header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
                }
        response = requests.get("https://tools.ipip.net/dns.php?a=dig&host=%s&custom_dns=&area[]=north_america"%hostname,headers=header)
        pattern = re.compile(r"parent.call_dns\((.*?)\);")
        r = pattern.findall(response.text)
        r = eval("["+r[0]+"]")
        for i in r[3]["ips"]:
            try:
                requests.get("http://" + i)
                self.hosts = "https://" + i
                return i
            except:
                pass
