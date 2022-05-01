# -*- coding:utf-8 -*-

from __future__ import annotations

from typing import Any

import requests
from requests_toolbelt.adapters import host_header_ssl  # type: ignore[import]

from .aapi import AppPixivAPI

# from typeguard import typechecked


# @typechecked
class ByPassSniApi(AppPixivAPI):
    def __init__(self, **requests_kwargs: Any) -> None:
        """initialize requests kwargs if need be"""
        super(AppPixivAPI, self).__init__(**requests_kwargs)
        session = requests.Session()
        session.mount("https://", host_header_ssl.HostHeaderSSLAdapter())
        self.requests = session

    def require_appapi_hosts(
        self, hostname: str = "app-api.pixiv.net", timeout: int = 3
    ) -> str | bool:
        """
        通过 DoH 服务请求真实的 IP 地址。
        """
        URLS = (
            "https://1.0.0.1/dns-query",
            "https://1.1.1.1/dns-query",
            "https://doh.dns.sb/dns-query",
            "https://cloudflare-dns.com/dns-query",
        )
        headers = {"Accept": "application/dns-json"}
        params = {
            "name": hostname,
            "type": "A",
            "do": "false",
            "cd": "false",
        }

        for url in URLS:
            try:
                response = requests.get(
                    url, headers=headers, params=params, timeout=timeout
                )
                self.hosts = "https://" + str(response.json()["Answer"][0]["data"])
                return self.hosts
            except Exception:
                pass

        return False
