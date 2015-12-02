PixivPy [![Build Status](https://travis-ci.org/upbit/pixivpy.svg)](https://travis-ci.org/upbit/pixivpy)
======
_Pixiv API for Python (with Auth supported)_

* [2015/08/11] Remove SPAI and release v3.0 (pixivpy3) (Public-API with Search API)
* [2015/05/16] As Pixiv **deprecated** SAPI in recent days, push new Public-API **ranking_all**
* [2014/10/07] New framework, **SAPI / Public-API** supported (requests needed)

Use pip for installing:

~~~
pip install pixivpy
~~~

Requirements: [requests](https://pypi.python.org/pypi/requests)

### Example:

~~~python
from pixivpy3 import *

api = PixivAPI()
api.login("username", "password")

# get origin url
json_result = api.works(45455208)
illust = json_result.response[0]
print("origin url: %s" % illust.image_urls['large'])

# get ranking (page1)
json_result = api.ranking_all('daily')
ranking = json_result.response[0]
for illust in ranking.works:
	print("[%s] %s" % (illust.work.title, illust.work.image_urls.px_480mw))

# acquire a new bearer token after your current token expires
# time.sleep(3600)
api.auth()
~~~

### [Sniffer - Public API](https://github.com/upbit/pixivpy/wiki/sniffer)

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

### Public-API

[PAPI](https://github.com/upbit/pixivpy/blob/master/pixivpy3/api.py).*

~~~python
class PixivAPI(object):

	def bad_words(self):

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
	#   text - 标题
	#   exact_tag - 标签
	# order:
	#   desc - 新顺序
	#   asc - 旧顺序
	def search_works(self, query, page=1, per_page=30, mode='text',
		period='all', order='desc', sort='date'):

~~~

[Usage](https://github.com/upbit/pixivpy/blob/master/demo.py#L27):

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

## License

Feel free to use, reuse and abuse the code in this project.
