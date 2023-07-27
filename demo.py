#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time

from pixivpy3 import AppPixivAPI, PixivError

sys.dont_write_bytecode = True


# get your refresh_token, and replace _REFRESH_TOKEN
#  https://github.com/upbit/pixivpy/issues/158#issuecomment-778919084
_REFRESH_TOKEN = "0zeYA-PllRYp1tfrsq_w3vHGU1rPy237JMf5oDt73c4"
_TEST_WRITE = False

# If a special network environment is meet, please configure requests as you need.
# Otherwise, just keep it empty.
_REQUESTS_KWARGS = {
    # 'proxies': {
    #     'https': 'http://127.0.0.1:1087',
    # },
    # 'verify': False,       # PAPI use https, an easy way is disable requests SSL verify
}

# AppAPI start


def appapi_illust(aapi):
    json_result = aapi.illust_detail(59580629)
    print(json_result)
    illust = json_result.illust
    print(">>> {}, origin url: {}".format(illust.title, illust.image_urls["large"]))

    json_result = aapi.illust_comments(59580629)
    print(json_result)

    # (2020/01/28) Comment because 51815717 is deleted
    # json_result = aapi.ugoira_metadata(51815717)
    # print(json_result)
    # metadata = json_result.ugoira_metadata
    # print(">>> frames=%d %s" % (len(metadata.frames), metadata.zip_urls.medium))


def appapi_recommend(aapi):
    json_result = aapi.illust_recommended(bookmark_illust_ids=[59580629])
    print(json_result)
    illust = json_result.illusts[0]
    print(">>> {}, origin url: {}".format(illust.title, illust.image_urls["large"]))

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.illust_recommended(**next_qs)
        # print(json_result)
        illust = json_result.illusts[0]
        print("  > {}, origin url: {}".format(illust.title, illust.image_urls["large"]))

    json_result = aapi.illust_related(59580629)
    print(json_result)
    illust = json_result.illusts[0]
    print(">>> {}, origin url: {}".format(illust.title, illust.image_urls["large"]))

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.illust_related(**next_qs)
        # print(json_result)
        illust = json_result.illusts[0]
        print("  > {}, origin url: {}".format(illust.title, illust.image_urls["large"]))


def appapi_users(aapi):
    json_result = aapi.user_detail(275527)
    print(json_result)
    user = json_result.user
    print(
        "{}(@{}) region={}".format(user.name, user.account, json_result.profile.region)
    )

    json_result = aapi.user_illusts(275527)
    print(json_result)
    illust = json_result.illusts[0]
    print(">>> {}, origin url: {}".format(illust.title, illust.image_urls["large"]))

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.user_illusts(**next_qs)
        # print(json_result)
        illust = json_result.illusts[0]
        print("  > {}, origin url: {}".format(illust.title, illust.image_urls["large"]))

    json_result = aapi.user_bookmarks_illust(2088434)
    print(json_result)
    illust = json_result.illusts[0]
    print(">>> {}, origin url: {}".format(illust.title, illust.image_urls["large"]))

    json_result = aapi.user_following(7314824)
    print(json_result)
    user_preview = json_result.user_previews[0]
    print(">>> {}(@{})".format(user_preview.user.name, user_preview.user.account))

    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.user_following(**next_qs)
        # print(json_result)
        user_preview = json_result.user_previews[0]
        print("  > {}(@{})".format(user_preview.user.name, user_preview.user.account))

    json_result = aapi.user_follower(275527)
    print(json_result)

    json_result = aapi.user_mypixiv(275527)
    print(json_result)

    json_result = aapi.user_related(275527)
    print(json_result)


def appapi_search(aapi):
    first_tag = None
    response = aapi.trending_tags_illust()
    for trend_tag in response.trend_tags[:10]:
        if not first_tag:
            first_tag = trend_tag.tag
        print(
            "%s -  %s(id=%s)"
            % (trend_tag.tag, trend_tag.illust.title, trend_tag.illust.id)
        )

    json_result = aapi.search_illust(first_tag, search_target="partial_match_for_tags")
    print(json_result)
    illust = json_result.illusts[0]
    print(">>> {}, origin url: {}".format(illust.title, illust.image_urls["large"]))

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.search_illust(**next_qs)
        # print(json_result)
        illust = json_result.illusts[0]
        print(">>> {}, origin url: {}".format(illust.title, illust.image_urls["large"]))

    # novel
    json_result = aapi.search_novel("FGO", search_target="keyword")
    print(json_result)
    novel = json_result.novels[0]
    print(">>> {}, origin url: {}".format(novel.title, novel.image_urls["large"]))

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.search_novel(**next_qs)
        # print(json_result)
        novel = json_result.novels[0]
        print(">>> {}, origin url: {}".format(novel.title, novel.image_urls["large"]))


def appapi_user_search(aapi):
    json_result = aapi.illust_ranking("day_male")
    name = json_result.illusts[0].user.name
    print(">>> %s" % name)

    json_result = aapi.search_user(name)
    print(json_result)
    illust = json_result.user_previews[0].illusts[0]
    print(">>> {}, origin url: {}".format(illust.title, illust.image_urls["large"]))

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.search_user(**next_qs)
        # print(json_result)
        illust = json_result.user_previews[0].illusts[0]
        print(">>> {}, origin url: {}".format(illust.title, illust.image_urls["large"]))


def appapi_ranking(aapi):
    json_result = aapi.illust_ranking("day_male")
    print(json_result)
    illust = json_result.illusts[0]
    print(">>> {}, origin url: {}".format(illust.title, illust.image_urls["large"]))

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.illust_ranking(**next_qs)
        # print(json_result)
        illust = json_result.illusts[0]
        print(">>> {}, origin url: {}".format(illust.title, illust.image_urls["large"]))

    # 2016-07-15 日的过去一周排行
    json_result = aapi.illust_ranking("week", date="2016-07-15")
    print(json_result)
    illust = json_result.illusts[0]
    print(">>> {}, origin url: {}".format(illust.title, illust.image_urls["large"]))


def appapi_auth_api(aapi):
    json_result = aapi.illust_follow(req_auth=True)
    print(json_result)
    illust = json_result.illusts[0]
    print(">>> {}, origin url: {}".format(illust.title, illust.image_urls["large"]))

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.illust_follow(req_auth=True, **next_qs)
        # print(json_result)
        illust = json_result.illusts[0]
        print(">>> {}, origin url: {}".format(illust.title, illust.image_urls["large"]))

    json_result = aapi.illust_recommended(req_auth=True)
    print(json_result)
    illust = json_result.illusts[0]
    print(">>> {}, origin url: {}".format(illust.title, illust.image_urls["large"]))


def appapi_bookmark_add(aapi):
    illust_id = 74187223
    tags = ["Fate/GO", "50000users入り", "私服"]
    json_result = aapi.illust_bookmark_add(illust_id, tags=tags)
    json_result = aapi.illust_bookmark_detail(illust_id)
    print(json_result.bookmark_detail)
    print(
        ">>> %s, tags added: %s"
        % (
            illust_id,
            [tag.name for tag in json_result.bookmark_detail.tags if tag.is_registered],
        )
    )


def appapi_novel(aapi):
    json_result = aapi.novel_recommended()
    print(json_result)
    novel = json_result.novels[0]
    print(
        ">>> %s, text_length: %s, series: %s"
        % (novel.title, novel.text_length, novel.series)
    )

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.novel_recommended(**next_qs)
        novel = json_result.novels[0]
        print(
            ">>> %s, text_length: %s, series: %s"
            % (novel.title, novel.text_length, novel.series)
        )

    json_result = aapi.user_novels(59216290)
    print(json_result)
    novel = json_result.novels[0]
    print(
        ">>> %s, text_length: %s, series: %s"
        % (novel.title, novel.text_length, novel.series)
    )

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.user_novels(**next_qs)
        novel = json_result.novels[0]
        print(
            ">>> %s, text_length: %s, series: %s"
            % (novel.title, novel.text_length, novel.series)
        )

    json_result = aapi.novel_series(1206600)
    print(json_result)
    detail = json_result.novel_series_detail
    print(
        ">>> %s, total_character_count: %s"
        % (detail.title, detail.total_character_count)
    )

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.novel_series(**next_qs)
        detail = json_result.novel_series_detail
        print(
            ">>> %s, total_character_count: %s"
            % (detail.title, detail.total_character_count)
        )

    novel_id = 12438689
    json_result = aapi.novel_detail(novel_id)
    print(json_result)
    novel = json_result.novel
    print(
        ">>> %s, text_length: %s, series: %s"
        % (novel.title, novel.text_length, novel.series)
    )

    json_result = aapi.novel_text(novel_id)
    print(json_result)
    print(">>> {}, novel_text: {}".format(novel.title, json_result.novel_text))

    json_result = aapi.novel_follow()
    print(json_result)
    novel = json_result.novels[0]
    print(
        ">>> %s, text_length: %s, series: %s"
        % (novel.title, novel.text_length, novel.series)
    )

def main():
    # app-api
    aapi = AppPixivAPI(**_REQUESTS_KWARGS)

    _e = None
    for _ in range(3):
        try:
            aapi.auth(refresh_token=_REFRESH_TOKEN)
            break
        except PixivError as e:
            _e = e
            time.sleep(10)
    else:  # failed 3 times
        raise _e

    appapi_illust(aapi)
    appapi_recommend(aapi)
    appapi_users(aapi)
    appapi_search(aapi)
    appapi_user_search(aapi)
    appapi_ranking(aapi)
    appapi_bookmark_add(aapi)
    appapi_novel(aapi)

    appapi_auth_api(aapi)


if __name__ == "__main__":
    main()
