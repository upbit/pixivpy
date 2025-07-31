from __future__ import annotations

import logging
from typing import Any

import requests
from requests_toolbelt.adapters import host_header_ssl  # type: ignore[unused-ignore]

from .aapi import AppPixivAPI

logger = logging.getLogger(__name__)


# @typechecked
class ByPassSniApi(AppPixivAPI):
    def __init__(self, **requests_kwargs: Any) -> None:
        """Initialize requests kwargs if need be"""
        super(AppPixivAPI, self).__init__(**requests_kwargs)
        session = requests.Session()
        session.mount("https://", host_header_ssl.HostHeaderSSLAdapter())
        self.requests = session

    def require_appapi_hosts(
        self, hostname: str = "app-api.secure.pixiv.net", timeout: int = 3
    ) -> str | bool:
        """通过 DoH 服务请求真实的 IP 地址。"""
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
                response.raise_for_status()  # 检查HTTP状态码

                # 解析JSON响应
                json_data = response.json()

                # 检查响应格式
                if "Answer" not in json_data or not json_data["Answer"]:
                    logger.debug(f"No Answer field in response from '{url}'")
                    continue

                domain_data = json_data["Answer"][0]["data"]
                self.hosts = f"https://{domain_data}"
                logger.info(
                    f"Successfully resolved {hostname} to {domain_data} via {url}"
                )
                return self.hosts

            except (requests.exceptions.JSONDecodeError, KeyError, IndexError) as e:
                logger.debug(
                    f"Unable to parse response from '{url}': {e}",
                    exc_info=True,
                )
            except requests.ConnectionError as e:
                logger.debug(
                    f"Unable to establish connection to '{url}': {e}",
                    exc_info=True,
                )
            except requests.RequestException as e:
                logger.debug(
                    f"Request failed for '{url}': {e}",
                    exc_info=True,
                )

        logger.warning(f"Failed to resolve {hostname} via any DoH service")
        return False
