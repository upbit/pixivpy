#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
if sys.version_info >= (3, 0):
    import imp
    imp.reload(sys)
else:
    reload(sys)
    sys.setdefaultencoding('utf8')
sys.dont_write_bytecode = True

from pixivpy3 import *

_REQUESTS_KWARGS = {
  # 'proxies': {
  #   'https': 'http://127.0.0.1:8888',
  # },
  # 'verify': False,       # PAPI use https, an easy way is disable requests SSL verify
}

def main():
    aapi = AppPixivAPI(**_REQUESTS_KWARGS)
    json_result = aapi.illust_ranking('day', date='2016-08-01')

    directory = "dl"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # download top3 day rankings to 'dl' dir
    for illust in json_result.illusts[:3]:
        image_url = illust.meta_single_page.get('original_image_url', illust.image_urls.large)
        print("%s: %s" % (illust.title, image_url))
        # aapi.download(image_url)

        url_basename = os.path.basename(image_url)
        extension = os.path.splitext(url_basename)[1]
        name = "illust_id_%d_%s%s" % (illust.id, illust.title, extension)
        aapi.download(image_url, path=directory, name=name)

if __name__ == '__main__':
    main()
