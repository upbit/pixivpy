#!/usr/bin/env python
from __future__ import annotations

import sys
import time
from typing import Any

from pixivpy3 import AppPixivAPI, PixivError

sys.dont_write_bytecode = True

# get your refresh_token, and replace _REFRESH_TOKEN
#  https://github.com/upbit/pixivpy/issues/158#issuecomment-778919084
_REFRESH_TOKEN = "<your_refresh_token>"
_TEST_WRITE = False

# If a special network environment is meet, please configure requests as you need.
# Otherwise, just keep it empty.
_REQUESTS_KWARGS: dict[str, Any] = {
    # 'proxies': {
    #     'https': 'http://127.0.0.1:1087',
    # },
    # 'verify': False,       # PAPI use https, an easy way is disable requests SSL verify
}


# AppAPI start


def appapi_illust(aapi: AppPixivAPI) -> None:
    json_result = aapi.illust_detail(59580629)
    print(json_result)
    illust = json_result.illust
    print(f">>> {illust.title}, origin url: {illust.image_urls.large}")

    json_result = aapi.illust_comments(59580629)
    print(json_result)

    # (2020/01/28) Comment because 51815717 is deleted
    # json_result = aapi.ugoira_metadata(51815717)
    # print(json_result)
    # metadata = json_result.ugoira_metadata
    # print(f">>> frames={len(metadata.frames)} {metadata.zip_urls.medium}")


def appapi_recommend(aapi: AppPixivAPI) -> None:
    json_result = aapi.illust_recommended(bookmark_illust_ids=[59580629])
    print(json_result)
    illust = json_result.illusts[0]
    print(f">>> {illust.title}, origin url: {illust.image_urls.large}")

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.illust_recommended(**next_qs)
        # print(json_result)
        illust = json_result.illusts[0]
        print(f"  > {illust.title}, origin url: {illust.image_urls.large}")

    json_result = aapi.illust_related(59580629)
    print(json_result)
    illust = json_result.illusts[0]
    print(f">>> {illust.title}, origin url: {illust.image_urls.large}")

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.illust_related(**next_qs)
        # print(json_result)
        illust = json_result.illusts[0]
        print(f"  > {illust.title}, origin url: {illust.image_urls.large}")


def appapi_users(aapi: AppPixivAPI) -> None:
    json_result = aapi.user_detail(275527)
    print(json_result)
    user = json_result.user
    print(f"{user.name}(@{user.account}) region={json_result.profile.region}")

    json_result = aapi.user_illusts(275527)
    print(json_result)
    illust = json_result.illusts[0]
    print(f">>> {illust.title}, origin url: {illust.image_urls.large}")

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.user_illusts(**next_qs)
        # print(json_result)
        illust = json_result.illusts[0]
        print(f"  > {illust.title}, origin url: {illust.image_urls.large}")

    json_result = aapi.user_bookmarks_illust(2088434)
    print(json_result)
    illust = json_result.illusts[0]
    print(f"  > {illust.title}, origin url: {illust.image_urls.large}")

    json_result = aapi.user_bookmarks_novel(42862448)
    print(json_result)
    novel = json_result.novels[0]
    print(f">>> {novel.title}, text_length: {novel.text_length}, series: {novel.series}")

    json_result = aapi.user_following(7314824)
    print(json_result)
    user_preview = json_result.user_previews[0]
    print(f">>> {user_preview.user.name}(@{user_preview.user.account})")

    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.user_following(**next_qs)
        # print(json_result)
        user_preview = json_result.user_previews[0]
        print(f">>> {user_preview.user.name}(@{user_preview.user.account})")

    json_result = aapi.user_follower(275527)
    print(json_result)

    json_result = aapi.user_mypixiv(275527)
    print(json_result)

    json_result = aapi.user_related(275527)
    print(json_result)

    json_result = aapi.user_bookmark_tags_illust(9373351)
    print(json_result)


def appapi_search(aapi: AppPixivAPI) -> None:
    first_tag: str = ""
    response = aapi.trending_tags_illust()
    for trend_tag in response.trend_tags[:10]:
        if not first_tag:
            first_tag = trend_tag.tag
        print(f"{trend_tag.tag} -  {trend_tag.illust.title}(id={trend_tag.illust.id})")

    json_result = aapi.search_illust(first_tag, search_target="partial_match_for_tags")
    print(json_result)
    illust = json_result.illusts[0]
    print(f">>> {illust.title}, origin url: {illust.image_urls.large}")

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.search_illust(**next_qs)
        # print(json_result)
        illust = json_result.illusts[0]
        print(f">>> {illust.title}, origin url: {illust.image_urls.large}")

    # novel
    json_result = aapi.search_novel("FGO", search_target="keyword")
    print(json_result)
    novel = json_result.novels[0]
    print(f">>> {illust.title}, origin url: {illust.image_urls.large}")

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.search_novel(**next_qs)
        # print(json_result)
        novel = json_result.novels[0]
        print(f">>> {novel.title}, origin url: {novel.image_urls['large']}")

    json_result = aapi.search_illust("AI生成", search_target="exact_match_for_tags", search_ai_type=0)
    # 关闭AI搜索选项后,将过滤掉所有illust_ai_type=2的插画,而illust_ai_type=1 or 0 的插画将被保留
    # 但是,加入了"AI生成"的tag却没有在作品提交时打开“AI生成”的开关的作品不会被筛选出结果列表
    print(json_result.illusts[0])


def appapi_user_search(aapi: AppPixivAPI) -> None:
    json_result = aapi.illust_ranking("day_male")
    name = json_result.illusts[0].user.name
    print(f">>> {name}")

    json_result = aapi.search_user(name)
    print(json_result)
    illust = json_result.user_previews[0].illusts[0]
    print(f">>> {illust.title}, origin url: {illust.image_urls.large}")

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.search_user(**next_qs)
        # print(json_result)
        illust = json_result.user_previews[0].illusts[0]
        print(f">>> {illust.title}, origin url: {illust.image_urls.large}")


def appapi_ranking(aapi: AppPixivAPI) -> None:
    json_result = aapi.illust_ranking("day_male")
    print(json_result)
    illust = json_result.illusts[0]
    print(f">>> {illust.title}, origin url: {illust.image_urls.large}")

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.illust_ranking(**next_qs)
        # print(json_result)
        illust = json_result.illusts[0]
        print(f">>> {illust.title}, origin url: {illust.image_urls.large}")

    # 2016-07-15 日的过去一周排行
    json_result = aapi.illust_ranking("week", date="2016-07-15")
    print(json_result)
    illust = json_result.illusts[0]
    print(f">>> {illust.title}, origin url: {illust.image_urls.large}")


def appapi_auth_api(aapi: AppPixivAPI) -> None:
    json_result = aapi.illust_follow(req_auth=True)
    print(json_result)
    illust = json_result.illusts[0]
    print(f">>> {illust.title}, origin url: {illust.image_urls.large}")

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.illust_follow(req_auth=True, **next_qs)
        # print(json_result)
        illust = json_result.illusts[0]
        print(f">>> {illust.title}, origin url: {illust.image_urls.large}")

    json_result = aapi.illust_recommended(req_auth=True)
    print(json_result)
    illust = json_result.illusts[0]
    print(f">>> {illust.title}, origin url: {illust.image_urls.large}")


def appapi_bookmark_add(aapi: AppPixivAPI) -> None:
    illust_id = 74187223
    tags = ["Fate/GO", "50000users入り", "私服"]
    aapi.illust_bookmark_add(illust_id, tags=tags)
    json_result = aapi.illust_bookmark_detail(illust_id)
    print(json_result.bookmark_detail)
    tags_added = [tag.name for tag in json_result.bookmark_detail.tags if tag.is_registered]
    print(f">>> {illust_id}, tags added: {tags_added}")


def appapi_novel(aapi: AppPixivAPI) -> None:
    json_result = aapi.novel_recommended()
    print(json_result)
    novel = json_result.novels[0]
    print(f">>> {novel.title}, text_length: {novel.text_length}, series: {novel.series}")

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.novel_recommended(**next_qs)
        novel = json_result.novels[0]
        print(f">>> {novel.title}, text_length: {novel.text_length}, series: {novel.series}")

    json_result = aapi.user_novels(59216290)
    print(json_result)
    novel = json_result.novels[0]
    print(f">>> {novel.title}, text_length: {novel.text_length}, series: {novel.series}")

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.user_novels(**next_qs)
        novel = json_result.novels[0]
        print(f">>> {novel.title}, text_length: {novel.text_length}, series: {novel.series}")

    json_result = aapi.novel_series(1206600)
    print(json_result)
    detail = json_result.novel_series_detail
    print(f">>> {detail.title}, total_character_count: {detail.total_character_count}")

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = aapi.novel_series(**next_qs)
        detail = json_result.novel_series_detail
        print(f">>> {detail.title}, total_character_count: {detail.total_character_count}")

    novel_id = 12438689
    json_result = aapi.novel_detail(novel_id)
    print(json_result)
    novel = json_result.novel
    print(f">>> {novel.title}, text_length: {novel.text_length}, series: {novel.series}")

    json_result = aapi.novel_text(novel_id)
    print(json_result)
    print(f">>> {novel.title}, novel_text: {json_result.novel_text}")

    json_result = aapi.novel_follow()
    print(json_result)
    novel = json_result.novels[0]
    print(f">>> {novel.title}, text_length: {novel.text_length}, series: {novel.series}")

    # List the comments of the novel
    json_result = aapi.novel_comments(16509454, include_total_comments=True)
    print(f"Total comments = {json_result.total_comments}")
    for comment in json_result.comments:
        if comment.parent_comment:
            text = (
                f"{comment.user.name} replied to {comment.parent_comment.user.name} at {comment.date} :"
                f" {comment.comment}"
            )
            print(text)
        else:
            text = f"{comment.user.name} at {comment.date} : {comment.comment}"
            print(text)


def main() -> None:
    # app-api
    aapi = AppPixivAPI(**_REQUESTS_KWARGS)

    er: Exception | None = None
    for _ in range(3):
        try:
            aapi.auth(refresh_token=_REFRESH_TOKEN)
            break
        except PixivError as e:
            er = e
            time.sleep(10)
    else:  # failed 3 times
        assert isinstance(er, Exception)
        raise er

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
