#!/usr/bin/env python

import os
import sys

from pixivpy3 import AppPixivAPI, ByPassSniApi, enums

sys.dont_write_bytecode = True


# get your refresh_token, and replace _REFRESH_TOKEN
#  https://github.com/upbit/pixivpy/issues/158#issuecomment-778919084
_REFRESH_TOKEN = "<your_refresh_token>"


def main() -> None:
    sni = False
    if not sni:
        api = AppPixivAPI()
    else:
        api = ByPassSniApi()  # Same as AppPixivAPI, but bypass the GFW
        api.require_appapi_hosts()
    api.auth(refresh_token=_REFRESH_TOKEN)

    # get rankings
    json_result = api.illust_ranking(enums.RankingMode.DAY, date="2019-01-01")

    directory = "illusts"
    if not os.path.exists(directory):
        os.makedirs(directory)  # noqa: PTH103

    # download top3 day rankings to 'illusts' dir
    for idx, illust in enumerate(json_result.illusts[:4]):
        image_url = illust.meta_single_pageoriginal_image_url or illust.image_urls.large
        print(f"{illust.title}: {image_url}")

        # try four args in MR#102
        if idx == 0:
            api.download(image_url, path=directory, name=None)
        elif idx == 1:
            url_basename = os.path.basename(image_url)
            extension = os.path.splitext(url_basename)[1]  # noqa: PTH122
            name = f"illust_id_{illust.id}_{illust.title}{extension}"
            api.download(image_url, path=directory, name=name)
        elif idx == 2:  # noqa: PLR2004; Valid, but I don't know myself
            fname = f"illust_{illust.id}.jpg"
            api.download(image_url, path=directory, fname=fname)
        else:
            # path will not work due to fname is a handler
            fname = f"{directory}/illust_{illust.id}.jpg"
            api.download(
                image_url,
                path="/foo/bar",
                fname=open(fname, "wb"),  # noqa: SIM115
            )


if __name__ == "__main__":
    main()
