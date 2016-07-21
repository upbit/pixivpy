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

## change _USERNAME,_PASSWORD first!
_USERNAME = "usersp"
_PASSWORD = "passsp"
_TEST_WRITE = False

## If a special network environment is met, please configure requests as you need.
## Otherwise, just keep it empty.
_REQUESTS_KWARGS = {
  # 'proxies': {
  #   'https': 'http://127.0.0.1:8888',
  # },
  # 'verify': False,       # PAPI use https, an easy way is disable requests SSL verify
}

def migrate_rev2_to_papi(api):
    print(">>> new ranking_all(mode='daily', page=1, per_page=50)")
    # rank_list = api.sapi.ranking("all", 'day', 1)
    rank_list = api.ranking_all('daily', 1, 50)
    print(rank_list)

    # more fields about response: https://github.com/upbit/pixivpy/wiki/sniffer
    ranking = rank_list.response[0]
    for img in ranking.works:
        # print img.work
        print("[%s/%s(id=%s)] %s" % (img.work.user.name, img.work.title, img.work.id, img.work.image_urls.px_480mw))

## PAPI start

def papi_base(api):
    # PAPI.works
    json_result = api.works(46363414)
    print(json_result)
    illust = json_result.response[0]
    print(">>> %s, origin url: %s" % (illust.caption, illust.image_urls['large']))

    # PAPI.users
    json_result = api.users(1184799)
    print(json_result)
    user = json_result.response[0]
    print(user.profile.introduction)


def papi_me(api):
    # PAPI.me_feeds
    json_result = api.me_feeds(show_r18=0)
    print(json_result)
    # work = json_result.response[0].ref_user.works[0]
    # print(work.title)

    # PAPI.me_favorite_works
    json_result = api.me_favorite_works(publicity='private')
    print(json_result)
    illust = json_result.response[0].work
    print("[%s] %s: %s" % (illust.user.name, illust.title, illust.image_urls.px_480mw))

    # PAPI.me_following_works (New -> Follow)
    json_result = api.me_following_works()
    print(json_result)
    illust = json_result.response[0]
    print(">>> %s, origin url: %s" % (illust.caption, illust.image_urls['large']))

    if _TEST_WRITE:
        # PAPI.me_favorite_works_add
        json_result = api.me_favorite_works_add(ref_work.id, publicity='private')
        print(json_result)
        favorite_id = json_result.response[0].id
        print(">>> Add favorite illust_id=%s success! favorite_id=%s" % (ref_work.id, favorite_id))

        # PAPI.me_favorite_works_delete
        # json_result = api.me_favorite_works_delete([favorite_id, ...], publicity='private')
        json_result = api.me_favorite_works_delete(favorite_id, publicity='private')
        print(json_result)


def papi_me_user(api):
    # PAPI.me_following
    json_result = api.me_following()
    print(json_result)
    user = json_result.response[0]
    print(user.name)

    if _TEST_WRITE:
        # PAPI.me_favorite_users_follow
        user_id = 1184799
        json_result = api.me_favorite_users_follow(user_id)
        print(json_result)
        user = json_result.response[0].target_user
        print(user.name)

        # PAPI.me_favorite_users_unfollow
        json_result = api.me_favorite_users_unfollow(user_id)
        print(json_result)


def papi_user(api):
    # PAPI.users_works
    json_result = api.users_works(1184799)
    print(json_result)
    illust = json_result.response[0]
    print(">>> %s, origin url: %s" % (illust.caption, illust.image_urls['large']))

    # PAPI.users_favorite_works
    json_result = api.users_favorite_works(1184799)
    print(json_result)
    illust = json_result.response[0].work
    print(">>> %s origin url: %s" % (illust.caption, illust.image_urls['large']))

    # PAPI.users_feeds
    json_result = api.users_feeds(1184799, show_r18=0)
    print(json_result)
    ref_work = json_result.response[0].ref_work
    print(ref_work.title)

    # PAPI.users_following
    json_result = api.users_following(1184799)
    print(json_result)
    user = json_result.response[0]
    print(user.name)


def papi_ranking(api):
    # PAPI.ranking
    json_result = api.ranking('illust', 'weekly', 1)
    print(json_result)
    illust = json_result.response[0].works[0].work
    print(">>> %s origin url: %s" % (illust.title, illust.image_urls['large']))

    # PAPI.ranking(2015-05-01)
    json_result = api.ranking(ranking_type='all', mode='daily', page=1, date='2015-05-01')
    print(json_result)
    illust = json_result.response[0].works[0].work
    print(">>> %s origin url: %s" % (illust.title, illust.image_urls['large']))


def papi_search(api):
    # PAPI.search_works
    json_result = api.search_works("五航戦 姉妹", page=1, mode='text')
    # json_result = api.search_works("水遊び", page=1, mode='exact_tag')
    print(json_result)
    illust = json_result.response[0]
    print(">>> %s origin url: %s" % (illust.title, illust.image_urls['large']))


def papi_others(api):
    # PAPI.latest_works (New -> Everyone)
    json_result = api.latest_works()
    print(json_result)
    illust = json_result.response[0]
    print(">>> %s url: %s" % (illust.title, illust.image_urls.px_480mw))

## AppAPI start

def appapi_recommend(aapi):
    json_result = aapi.illust_recommended()
    print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

    json_result = aapi.illust_related(57065990)
    print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    json_result = aapi.illust_related(**next_qs)
    # print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

def appapi_users(aapi):
    json_result = aapi.user_detail(660788)
    print(json_result)
    user = json_result.user
    print("%s(@%s) region=%s" % (user.name, user.account, json_result.profile.region))

    json_result = aapi.user_illusts(660788)
    print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    json_result = aapi.user_illusts(**next_qs)
    # print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

def refresh_token(api):
    """Acquire a new bearer token after your current token expires,
    just call auth() or specifies a refresh_token
    """
    print("refresh_token before: %s" % api.refresh_token)

    # api.auth(refresh_token = api.refresh_token)
    api.auth()

    print("refresh_token  after: %s" % api.refresh_token)


def main():
    # api = PixivAPI()
    api = PixivAPI(**_REQUESTS_KWARGS)
    api.login(_USERNAME, _PASSWORD)

    migrate_rev2_to_papi(api)

    papi_base(api)
    papi_me(api)
    papi_me_user(api)
    papi_user(api)
    papi_ranking(api)
    papi_search(api)
    papi_others(api)

    # app-api (experimental)
    aapi = AppPixivAPI(**_REQUESTS_KWARGS)
    aapi.login(_USERNAME, _PASSWORD)

    appapi_recommend(aapi)
    appapi_users(aapi)

    # Because issues #12, Pixiv return 1508 when use refresh_token
    # Disable refresh_token before found a new solution
    # refresh_token(api)

if __name__ == '__main__':
    main()
