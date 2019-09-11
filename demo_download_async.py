#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import os

from pixivpy3.aio import AppPixivAPI

_USERNAME = "userbay"
_PASSWORD = "userpay"


async def _main(aapi):
    await aapi.login(_USERNAME, _PASSWORD)
    json_result = await aapi.illust_ranking('day', date='2016-08-01')

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
        await aapi.download(image_url, path=directory, name=name)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(AppPixivAPI()))


if __name__ == '__main__':
    main()