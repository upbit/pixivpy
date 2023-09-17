import sys
from datetime import datetime, timedelta

from pixivpy3 import ByPassSniApi

sys.dont_write_bytecode = True


# get your refresh_token, and replace _REFRESH_TOKEN
#  https://github.com/upbit/pixivpy/issues/158#issuecomment-778919084
_REFRESH_TOKEN = "0zeYA-PllRYp1tfrsq_w3vHGU1rPy237JMf5oDt73c4"


def main():
    api = ByPassSniApi()  # Same as AppPixivAPI, but bypass the GFW
    # api.require_appapi_hosts()
    api.require_appapi_hosts(hostname="public-api.secure.pixiv.net")
    # api.set_additional_headers({'Accept-Language':'en-US'})
    api.set_accept_language("en-us")

    # api.login(_USERNAME, _PASSWORD)
    print(api.auth(refresh_token=_REFRESH_TOKEN))
    json_result = api.illust_ranking("day", date=(datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"))

    print("Printing image titles and tags with English tag translations present when available")

    for illust in json_result.illusts[:3]:
        print('Illustration: "' + str(illust.title) + '"\nTags: ' + str(illust.tags) + "\n")


if __name__ == "__main__":
    main()
