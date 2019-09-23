# -*- coding: utf-8 -*-
import sys

from pixivpy3.bapi import ByPassSniApi

if sys.version_info >= (3, 0):
    import imp

    imp.reload(sys)
else:
    reload(sys)
    sys.setdefaultencoding('utf8')
sys.dont_write_bytecode = True

from pixivpy3 import *
from datetime import *

# change _USERNAME,_PASSWORD first!
_USERNAME = "userbay"
_PASSWORD = "userpay"


def main():
    bapi = ByPassSniApi()
    bapi.require_appapi_hosts()
    # bapi.set_additional_headers({'Accept-Language':'en-US'})
    bapi.set_accept_language('en-us')  # zh-cn

    bapi.login(_USERNAME, _PASSWORD)
    json_result = bapi.illust_ranking('day', date=(datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'))

    print("Printing image titles and tags with English tag translations present when available")

    for illust in json_result.illusts[:3]:
        print("Illustration: \"" + str(illust.title) + "\"\nTags: " + str(illust.tags) + "\n")


if __name__ == '__main__':
    main()
