# -*- coding:utf-8 -*-

from typing import Any, Union

import requests
from requests_toolbelt.adapters import host_header_ssl  # type: ignore[import]
from typeguard import typechecked

from .aapi import AppPixivAPI


@typechecked
class ByPassSniApi(AppPixivAPI):
    def __init__(self, **requests_kwargs: Any) -> None:
        """initialize requests kwargs if need be"""
        super(AppPixivAPI, self).__init__(**requests_kwargs)
        session = requests.Session()
        session.mount("https://", host_header_ssl.HostHeaderSSLAdapter())
        self.requests = session

    def require_appapi_hosts(
        self, hostname: str = "app-api.pixiv.net", timeout: int = 3
    ) -> Union[str, bool]:
        """
        通过 DNS over HTTPS 服务获取真实 IP 地址。
        """
        URLS = (
            "https://1.0.0.1/dns-query",
            "https://dns.alidns.com/dns-query",
            "https://doh.dns.sb/dns-query",
            "https://doh.opendns.com/dns-query",
            "https://cloudflare-dns.com/dns-query",
            "https://dns.google/dns-query"
        )
        params = {
            "ct": "application/dns-json",
            "name": hostname,
            "type": "A",
            "do": "false",
            "cd": "false",
        }

        for url in URLS:
            try:
                response = requests.get(url, params=params, timeout=timeout)
                self.hosts = "https://" + str(response.json()["Answer"][0]["data"])
                return self.hosts
            except Exception:
                pass

        return False
