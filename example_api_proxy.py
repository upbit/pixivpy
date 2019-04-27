#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
if sys.version_info >= (3, 0):
    import imp
    imp.reload(sys)
else:
    reload(sys)
    sys.setdefaultencoding('utf8')
sys.dont_write_bytecode = True

from pixivpy3 import *

# change _USERNAME,_PASSWORD first!
_USERNAME = "userbay"
_PASSWORD = "userpay"


def proxy_get_tokens():
    aapi = AppPixivAPI(proxies={'https': 'http://127.0.0.1:1087'}, verify=False)
    return aapi.login(_USERNAME, _PASSWORD)


def main():
    # use proxy get tokens
    tokens = proxy_get_tokens()

    aapi = AppPixivAPI() # no proxy needed
    aapi.set_auth(tokens.response.access_token)

    # set API proxy to pixivlite.com
    aapi.set_api_proxy("http://app-api.pixivlite.com")

    json_result = aapi.illust_ranking('day')
    print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))


if __name__ == '__main__':
    main()
