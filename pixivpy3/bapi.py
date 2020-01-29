# -*- coding:utf-8 -*-

import requests
from requests_toolbelt.adapters import host_header_ssl

from .aapi import AppPixivAPI


class ByPassSniApi(AppPixivAPI):

    def __init__(self, **requests_kwargs):
        """initialize requests kwargs if need be"""
        super(AppPixivAPI, self).__init__(**requests_kwargs)
        session = requests.Session()
        session.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
        self.requests = session

    def require_appapi_hosts(self, hostname="app-api.pixiv.net", timeout=3):
        """
        通过cloudflare的 DNS over HTTPS 请求真实的ip地址
        """
        url = "https://1.0.0.1/dns-query"   # 先使用1.0.0.1的地址
        params = {
            'ct': 'application/dns-json',
            'name': hostname,
            'type': 'A',
            'do': 'false',
            'cd': 'false',
        }

        try:
            response = requests.get(url, params=params, timeout=timeout)
        except Exception:
            # 根据 #111 的反馈，部分地区无法访问1.0.0.1，此时尝试域名解析
            url = "https://cloudflare-dns.com/dns-query"
            response = requests.get(url, params=params, timeout=timeout)

        # 返回第一个解析到的IP
        self.hosts = "https://" + response.json()['Answer'][0]['data']
        return self.hosts
