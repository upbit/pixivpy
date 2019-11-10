PixivPy [![Build Status](https://travis-ci.org/upbit/pixivpy.svg)](https://travis-ci.org/upbit/pixivpy) [![PyPI version](https://badge.fury.io/py/PixivPy.svg)](https://badge.fury.io/py/PixivPy)
======
_Pixiv API for Python (with Auth supported)_

* [2019/09/23] 增加大陆地区AppAPI的免翻墙访问支持, release v3.5 (See [example_bypass_sni.py](https://github.com/upbit/pixivpy/blob/master/example_bypass_sni.py), thanks [@Notsfsssf](https://github.com/Notsfsssf))
* [2019/09/03] Support new auth() check `X-Client-Time/X-Client-Hash` (thanks [DaRealFreak](https://github.com/DaRealFreak), [#83](https://github.com/upbit/pixivpy/issues/83))
* [2019/04/27] Support hosts proxy for AppAPI, which can use behind the Great Wall (See [example_api_proxy.py](https://github.com/upbit/pixivpy/blob/master/example_api_proxy.py))
* [2017/04/18] Fix encoder BUG for `illust_bookmark_add()/illust_bookmark_delete()` params (thanks [naplings](https://github.com/naplings))
* [2017/01/05] Add `PixivAPI().works()` liked API `illust_detail()` for App-API (thanks [Mapaler](https://github.com/Mapaler)), release v3.3
* [2016/12/17] Fixed encoding BUG for Public-API, see #26 (thanks [Xdynix](https://github.com/Xdynix))
* [2016/07/27] Now `AppPixivAPI()` can call **without auth** (thanks [zzycami](https://github.com/zzycami)), check [demo.py](https://github.com/upbit/pixivpy/blob/b83578e066ddcba86295676d931ff3313d138b22/demo.py#L268)
* [2016/07/20] New **App-API** (Experimental) for `PixivIOSApp/6.0.9`
* [2016/07/11] Add new [iOS 6.x API](https://github.com/upbit/pixivpy/wiki#6x-api) reference to Wiki
* [2015/12/02] Add write API for favorite an user / illust, release v3.1
* [2015/08/11] Remove SPAI and release v3.0 (pixivpy3) (Public-API with Search API)
* [2015/05/16] As Pixiv **deprecated** SAPI in recent days, push new Public-API **ranking_all**
* [2014/10/07] New framework, **SAPI / Public-API** supported (requests needed)

Use pip for installing:

~~~
pip install pixivpy --upgrade
~~~

Requirements: [requests](https://pypi.python.org/pypi/requests)

### [Mikubill/PixivPy-Async](https://github.com/Mikubill/pixivpy-async): Async Pixiv API for Python 3

性能对比（需要高性能访问场景，可以参考[这个脚本](https://github.com/Mikubill/pixivpy-async/blob/master/Perf.py)）

@Mikubill: 简单进行了一下并发测试。（撞了N次Rate Limit...)

`sg -> Singapore, jp -> Japan, unit -> second`

| Method | Sync(10,sg)  |  Async(10,sg)   |  Sync(200,sg)  |  Async(200,sg)   |
| ----  | ----  |  ----  | ----  |  ----  | 
|  illust_detail  | 1.1209 | 0.8641 | 31.7041 | 2.4580 |
| illust_ranking  | 1.0697 | 0.7936 | 28.4539 | 2.0693 |
|   user_illusts  | 0.8824 | 0.7505 | 28.3981 | 1.8199 |
|    user_detail  | 0.9628 | 0.7550 | 28.3055 | 1.7738 |
| ugoira_metadata | 0.8509 | 0.7459 | 29.5566 | 2.2331 |
| works           | 1.1204 | 0.8912 | 32.2068 | 2.8513 |
| me_following_works | 1.1253 | 0.7845 | 39.3142 | 2.2785 |
| ranking             | 1.0946 | 0.7944 | 39.6509 | 2.6548 |
| latest_works        | 1.0483 | 0.8667 | 36.1992 | 2.5066 |


| Method |  Sync(500,jp)  |  Async(500,jp)   |  
| ----  |  ----  |  ----  | 
|  illust_detail  |6.2178 | 0.6400 |
| illust_ranking  |6.4046 | 0.6119 |
|   user_illusts  |7.6093 | 1.5266 |
|    user_detail  |6.6759 | 0.5952 |
| ugoira_metadata |6.5155 | 0.7577 |
| works           | 13.3074| 0.8619|
| me_following_works | 24.2693|2.0835|
| ranking             | 21.4119|3.2805|
| latest_works        | 17.3502|2.7029|

### Projects base on pixivpy

1. [Xdynix/PixivPixie](https://github.com/Xdynix/PixivPixie): User-friendly Pixiv API based on PixivPy
2. [Mikubill/PixivPy-Async](https://github.com/Mikubill/pixivpy-async): Async Pixiv API for Python 3

### Example:

~~~python
from pixivpy3 import *

api = AppPixivAPI()
# api.login("username", "password")   # Not required

# get origin url
json_result = api.illust_detail(59580629)
illust = json_result.illust
print(">>> origin url: %s" % illust.image_urls['large'])

# get ranking: 1-30
# mode: [day, week, month, day_male, day_female, week_original, week_rookie, day_manga]
json_result = api.illust_ranking('day')
for illust in json_result.illusts:
    print(" p1 [%s] %s" % (illust.title, illust.image_urls.medium))

# next page: 31-60
next_qs = api.parse_qs(json_result.next_url)
json_result = api.illust_ranking(**next_qs)
for illust in json_result.illusts:
    print(" p2 [%s] %s" % (illust.title, illust.image_urls.medium))
~~~

### [Sniffer - App API](https://github.com/upbit/pixivpy/wiki#6x-api)
### [Sniffer - Public API](https://github.com/upbit/pixivpy/wiki/sniffer)


### [Using API proxy behind the Great Wall](https://github.com/upbit/pixivpy/blob/master/example_api_proxy.py#L33) See detail in [Issue#73](https://github.com/upbit/pixivpy/issues/73)

1. Upgrade pixivpy >= **v3.2.0**: `pip install pixivpy --upgrade`
2. Call `api.download()` like the below:

~~~python
aapi = AppPixivAPI()
json_result = aapi.illust_ranking()
for illust in json_result.illusts[:3]:
    aapi.download(illust.image_urls.large)
~~~

### [Migrate pixivpy2 to pixivpy3](https://github.com/upbit/pixivpy/blob/master/demo.py#L15-L25)

1. Replace `api.papi.*` to `api.*`
2. Change deprecated SPAI call to Public-API call

~~~python
print(">>> new ranking_all(mode='daily', page=1, per_page=50)")
#rank_list = api.sapi.ranking("all", 'day', 1)
rank_list = api.ranking_all('daily', 1, 50)
print(rank_list)

# more fields about response: https://github.com/upbit/pixivpy/wiki/sniffer
ranking = rank_list.response[0]
for img in ranking.works:
	#print img.work
	print("[%s/%s(id=%s)] %s" % (img.work.user.name, img.work.title, img.work.id, img.work.image_urls.px_480mw))
~~~

### About

1. Blog: [Pixiv Public-API (OAuth)分析](http://blog.imaou.com/opensource/2014/10/09/pixiv_api_for_ios_update.html)

If you have any questions, please feel free to contact me: rmusique@gmail.com

Find Pixiv API in **Objective-C**? You might also like [**PixivAPI_iOS**](https://github.com/upbit/PixivAPI_iOS)

## API functions

### App-API (6.0 - app-api.pixiv.net)

~~~python
class AppPixivAPI(BasePixivAPI):

    # 返回翻页用参数
    def parse_qs(self, next_url):

    # 用户详情 
    def user_detail(self, user_id):

    # 用户作品列表 
    def user_illusts(self, user_id, type='illust'):

    # 用户收藏作品列表 
    def user_bookmarks_illust(self, user_id, restrict='public'):

    # 关注用户的新作
    # restrict: [public, private]
    def illust_follow(self, restrict='public'):

    # 作品详情 (无需登录，同PAPI.works)
    def illust_detail(self, illust_id):

    # 相关作品列表 
    def illust_related(self, illust_id):

    # 插画推荐 (Home - Main) 
    # content_type: [illust, manga]
    def illust_recommended(self, content_type='illust'):

    # 作品排行
    # mode: [day, week, month, day_male, day_female, week_original, week_rookie, day_manga]
    # date: '2016-08-01'
    # mode(r18榜单需登录): [day_r18, day_male_r18, day_female_r18, week_r18, week_r18g]
    def illust_ranking(self, mode='day', date=None, offset=None):

    # 趋势标签 (Search - tags) 
    def trending_tags_illust(self):

    # 搜索 (Search) 
    # search_target - 搜索类型
    #   partial_match_for_tags  - 标签部分一致
    #   exact_match_for_tags    - 标签完全一致
    #   title_and_caption       - 标题说明文
    # sort: [date_desc, date_asc]
    # duration: [within_last_day, within_last_week, within_last_month]
    def search_illust(self, word, search_target='partial_match_for_tags', sort='date_desc', duration=None):

    # 作品收藏详情 
    def illust_bookmark_detail(self, illust_id):

    # 新增收藏
    def illust_bookmark_add(self, illust_id, restrict='public', tags=None):

    # 删除收藏
    def illust_bookmark_delete(self, illust_id):

    # 用户收藏标签列表
    def user_bookmark_tags_illust(self, restrict='public', offset=None):

    # Following用户列表 
    def user_following(self, user_id, restrict='public', offset=None):

    # Followers用户列表 
    def user_follower(self, user_id, filter='for_ios', offset=None):

    # 好P友 
    def user_mypixiv(self, user_id, offset=None):

    # 黑名单用户 
    def user_list(self, user_id, filter='for_ios', offset=None):

    # 获取ugoira信息
    def ugoira_metadata(self, illust_id):
~~~

[Usage](https://github.com/upbit/pixivpy/blob/master/demo.py#L42):

~~~python
aapi = AppPixivAPI()

# 作品推荐
json_result = aapi.illust_recommended()
print(json_result)
illust = json_result.illusts[0]
print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

# 作品相关推荐
json_result = aapi.illust_related(57065990)
print(json_result)
illust = json_result.illusts[0]
print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

# 作品相关推荐-下一页 (.parse_qs(next_url) 用法)
next_qs = aapi.parse_qs(json_result.next_url)
json_result = aapi.illust_related(**next_qs)
print(json_result)
illust = json_result.illusts[0]
print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

# 用户详情
json_result = aapi.user_detail(660788)
print(json_result)
user = json_result.user
print("%s(@%s) region=%s" % (user.name, user.account, json_result.profile.region))

# 用户作品列表
json_result = aapi.user_illusts(660788)
print(json_result)
illust = json_result.illusts[0]
print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

# 用户收藏列表
json_result = aapi.user_bookmarks_illust(2088434)
print(json_result)
illust = json_result.illusts[0]
print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

# 2016-07-15 日的过去一周排行
json_result = aapi.illust_ranking('week', date='2016-07-15')
print(json_result)
illust = json_result.illusts[0]
print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

# 关注用户的新作 (需要login)
json_result = aapi.illust_follow(req_auth=True)
print(json_result)
illust = json_result.illusts[0]
print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

# 标签 "水着" 搜索
json_result = aapi.search_illust('水着', search_target='partial_match_for_tags')
print(json_result)
illust = json_result.illusts[0]
print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))
~~~

### Public-API

[PAPI](https://github.com/upbit/pixivpy/blob/master/pixivpy3/api.py).*

~~~python
class PixivAPI(BasePixivAPI):

	# 作品详细
	def works(self, illust_id):

	# 用户资料
	def users(self, author_id):

	# 我的订阅
	def me_feeds(self, show_r18=1):

	# 获取收藏夹
	def me_favorite_works(self,page=1,per_page=50,image_sizes=['px_128x128', 'px_480mw', 'large']):

	# 添加收藏
	# publicity:  public, private
	def me_favorite_works_add(self, work_id, publicity='public'):

	# 删除收藏
	def me_favorite_works_delete(self, ids):

	# 关注用户
	# publicity:  public, private
	def me_favorite_users_follow(self, user_id, publicity='public'):

	# 用户作品
	# publicity:  public, private
	def users_works(self, author_id, page=1, per_page=30, publicity='public'):

	# 用户收藏
	# publicity:  public, private
	def users_favorite_works(self, author_id, page=1, per_page=30, publicity='public'):

	# 排行榜/过去排行榜
	# mode:
	#   daily - 每日
	#   weekly - 每周
	#   monthly - 每月
	#   male - 男性热门
	#   female - 女性热门
	#   original - 原创
	#   rookie - Rookie
	#   daily_r18 - R18每日
	#   weekly_r18 - R18每周
	#   male_r18
	#   female_r18
	#   r18g
	# page: 1-n
	# date: '2015-04-01' (仅过去排行榜)
	def ranking_all(self, mode='daily', page=1, per_page=50, date=None):

	# 搜索
	# query: 搜索的文字
	# page: 1-n
	# mode:
	#   text - 标题/描述
	#   tag - 非精确标签
	#   exact_tag - 精确标签
	#   caption - 描述
	# period (only applies to asc order):  
	#   all - 所有
	#   day - 一天之内
	#   week - 一周之内
	#   month - 一月之内
	# order:
	#   desc - 新顺序
	#   asc - 旧顺序
	def search_works(self, query, page=1, per_page=30, mode='text',
		period='all', order='desc', sort='date'):

~~~

[Usage](https://github.com/upbit/pixivpy/blob/master/demo.py#L42):

~~~python
# 作品详细 PAPI.works
json_result = api.works(46363414)
print(json_result)
illust = json_result.response[0]
print( ">>> %s, origin url: %s" % (illust.caption, illust.image_urls['large']))

# 用户资料 PAPI.users
json_result = api.users(1184799)
print(json_result)
user = json_result.response[0]
print(user.profile.introduction)

# 我的订阅 PAPI.me_feeds
json_result = api.me_feeds(show_r18=0)
print(json_result)
ref_work = json_result.response[0].ref_work
print(ref_work.title)

# 我的收藏列表(private) PAPI.me_favorite_works
json_result = api.me_favorite_works(publicity='private')
print(json_result)
illust = json_result.response[0].work
print("[%s] %s: %s" % (illust.user.name, illust.title, illust.image_urls.px_480mw))

# 关注的新作品[New -> Follow] PAPI.me_following_works
json_result = api.me_following_works()
print(json_result)
illust = json_result.response[0]
print(">>> %s, origin url: %s" % (illust.caption, illust.image_urls['large']))

# 我关注的用户 PAPI.me_following
json_result = api.me_following()
print(json_result)
user = json_result.response[0]
print(user.name)

# 用户作品 PAPI.users_works
json_result = api.users_works(1184799)
print(json_result)
illust = json_result.response[0]
print(">>> %s, origin url: %s" % (illust.caption, illust.image_urls['large']))

# 用户收藏 PAPI.users_favorite_works
json_result = api.users_favorite_works(1184799)
print(json_result)
illust = json_result.response[0].work
print(">>> %s origin url: %s" % (illust.caption, illust.image_urls['large']))

# 获取收藏夹 PAPI.me_favorite_works
json_result = api.me_favorite_works()
print(json_result)
ids = json_result.response[0].id

# 添加收藏 PAPI.me_favorite_works_add
json_result = api.me_favorite_works_add(46363414)
print(json_result)

# 删除收藏 PAPI.me_favorite_works_delete
json_result = api.me_favorite_works_delete(ids)
print(json_result)

# 关注用户 PAPI.me_favorite_users_follow
json_result = api.me_favorite_users_follow(1184799)
print(json_result)

# 排行榜 PAPI.ranking(illust)
json_result = api.ranking('illust', 'weekly', 1)
print(json_result)
illust = json_result.response[0].works[0].work
print(">>> %s origin url: %s" % (illust.title, illust.image_urls['large']))

# 过去排行榜 PAPI.ranking(all, 2015-05-01)
json_result = api.ranking(ranking_type='all', mode='daily', page=1, date='2015-05-01')
print(json_result)
illust = json_result.response[0].works[0].work
print(">>> %s origin url: %s" % (illust.title, illust.image_urls['large']))

# 标题(text)/标签(exact_tag)搜索 PAPI.search_works
#json_result = api.search_works("五航戦 姉妹", page=1, mode='text')
json_result = api.search_works("水遊び", page=1, mode='exact_tag')
print(json_result)
illust = json_result.response[0]
print(">>> %s origin url: %s" % (illust.title, illust.image_urls['large']))

# 最新作品列表[New -> Everyone] PAPI.latest_works
json_result = api.latest_works()
print(json_result)
illust = json_result.response[0]
print(">>> %s url: %s" % (illust.title, illust.image_urls.px_480mw))
~~~

## Make a release

> Bump version in `pixivpy3/__init__.py`, rebuild dist/*

```bash
python3 setup.py sdist bdist_wheel
python2 setup.py bdist_wheel
twine upload dist/*
```

## License

Feel free to use, reuse and abuse the code in this project.
