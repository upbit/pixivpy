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

def test_illusts(message, response):
    """Helper function for output illusts"""
    illust = response.illusts[0]
    print("%s%s %s" % (message, illust.title, illust.image_urls.large))

def test_next_page(api, test_function, next_url):
    """Helper function for call next_url"""
    qs = api.parse_qs(next_url)
    response = test_function(**qs)
    test_illusts("   ", response)

# app-api test
def appapi_users(api):
    response = api.user_detail(660788)
    user = response.user
    print("%s(@%s) region=%s" % (user.name, user.account, response.profile.region))

    response = api.user_illusts(660788)
    test_illusts("+: ", response)
    test_next_page(api, api.user_illusts, response.next_url)

def appapi_recommend(api):
    response = api.illust_recommended()
    test_illusts("+: ", response)
    test_next_page(api, api.illust_recommended, response.next_url)

    response = api.illust_related(57065990)
    test_illusts("+: ", response)
    test_next_page(api, api.illust_related, response.next_url)

def main():
    api = AppPixivAPI()
    # api = AppPixivAPI(**_REQUESTS_KWARGS)
    api.login(_USERNAME, _PASSWORD)

    appapi_users(api)
    appapi_recommend(api)

if __name__ == '__main__':
    main()
