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

_USERNAME = "usersp"
_PASSWORD = "passsp"
_TEST_WRITE = False

_REQUESTS_KWARGS = {
    'proxies': {
        'https': 'http://192.168.88.167:8888',
    },
    'verify': False,       # PAPI use https, an easy way is disable requests SSL verify
}

def appapi_recommend(api):
    response = api.illust_recommended()
    illust = response.illusts[0]
    print("page1: %s %s" % (illust.title, illust.meta_single_page.original_image_url))

    # get next page
    qs = api.parse_qs(response.next_url)
    response = api.illust_recommended(**qs)
    illust = response.illusts[0]
    print("page2: %s %s" % (illust.title, illust.meta_single_page.original_image_url))

def main():
    api = AppPixivAPI()
    # api = AppPixivAPI(**_REQUESTS_KWARGS)
    api.login(_USERNAME, _PASSWORD)

    appapi_recommend(api)

if __name__ == '__main__':
    main()
