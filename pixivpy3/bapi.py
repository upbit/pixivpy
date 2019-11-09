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

    def require_appapi_hosts(self, hostname="app-api.pixiv.net"):
        """
        通过1.0.0.1请求真实的ip地址
        """
        url = "https://1.0.0.1/dns-query?ct=application/dns-json&name=%s&type=A&do=false&cd=false" % hostname
        response = requests.get(url)
        self.hosts = "https://" + response.json()['Answer'][0]['data']
