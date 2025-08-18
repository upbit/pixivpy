import sys
from datetime import datetime, timedelta

from pixivpy3 import ByPassSniApi, enums

sys.dont_write_bytecode = True


# get your refresh_token, and replace _REFRESH_TOKEN
#  https://github.com/upbit/pixivpy/issues/158#issuecomment-778919084
_REFRESH_TOKEN = "<your_refresh_token>"


def main() -> None:
    api = ByPassSniApi()  # Same as AppPixivAPI, but bypass the GFW
    api.require_appapi_hosts()
    # api.set_additional_headers({'Accept-Language':'en-US'})
    api.set_accept_language("en-us")

    # api.login(_USERNAME, _PASSWORD)
    print(api.auth(refresh_token=_REFRESH_TOKEN))
    date = datetime.now() - timedelta(days=5)
    json_result = api.illust_ranking(enums.RankingMode.DAY, date=date)

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
