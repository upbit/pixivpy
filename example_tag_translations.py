#!/usr/bin/env python

import sys
from datetime import datetime, timedelta

from pixivpy3 import AppPixivAPI, enums

sys.dont_write_bytecode = True


# get your refresh_token, and replace _REFRESH_TOKEN
#  https://github.com/upbit/pixivpy/issues/158#issuecomment-778919084
_REFRESH_TOKEN = "<your_refresh_token>"


def main() -> None:
    aapi = AppPixivAPI()
    # aapi.set_additional_headers({'Accept-Language':'en-US'})
    aapi.set_accept_language("en-us")  # zh-cn

    aapi.auth(refresh_token=_REFRESH_TOKEN)
    date = datetime.now() - timedelta(days=5)
    json_result = aapi.illust_ranking(enums.RankingMode.DAY, date=date)

    print(
        "Printing image titles and tags with English tag translations present when available"
    )

    for illust in json_result.illusts[:3]:
        print(
            'Illustration: "'
            + str(illust.title)
            + '"\nTags: '
            + str(illust.tags)
            + "\n"
        )


if __name__ == "__main__":
    main()
