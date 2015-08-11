PixivPy
======
_Pixiv API for Python (with Auth supported)_

* [2015/08/11] Remove SPAI and release v3.0 (pixivpy3) (Public-API with Search API)
* [2015/05/16] As Pixiv **deprecated** SAPI in recent days, push new Public-API **ranking_all**
* [2014/10/07] New framework, **SAPI / Public-API** supported (requests needed)

Requirements: [requests](https://pypi.python.org/pypi/requests), use pip to install:

~~~
pip install requests
~~~

### Example:

~~~python
api = PixivAPI()
api.login("username", "password")

# get origin url
json_result = api.get_works(45455208)
illust = json_result.response[0]
print "origin url: %s" % illust.image_urls['large']

# get ranking (page1)
json_result = api.ranking_all('daily')
ranking = json_result.response[0]
for illust in ranking.works:
	print "[%s] %s" % (illust.work.title, illust.work.image_urls.px_480mw)
~~~

### [Migrate pixivpy2 to pixivpy3](https://github.com/upbit/pixivpy/blob/master/demo.py#L15-L25)

1. Replace `api.papi.*` to `api.*`
2. Change deprecated SPAI call to Public-API call

~~~python
print(">>> new ranking_all(mode='daily', page=1, per_page=50)")
#rank_list = api.sapi.ranking("all", 'day', 1)
rank_list = api.ranking_all('daily', 1, 50)
print rank_list

# more fields about response: https://github.com/upbit/pixivpy/wiki/sniffer
ranking = rank_list.response[0]
for img in ranking.works:
	#print img.work
	print "[%s/%s(id=%s)] %s" % (img.work.user.name, img.work.title, img.work.id, img.work.image_urls.px_480mw)
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
	#		exact_tag - 标签
	#   text - 标题
	# order:
	#		desc - 新顺序
	#		asc - 旧顺序
	def search_works(self, query, page=1, per_page=30, mode='exact_tag',
		period='all', order='desc', sort='date'):

~~~

[Usage](https://github.com/upbit/pixivpy/blob/master/demo.py#L27):

~~~python
# 作品详细 PAPI.works
json_result = api.works(46363414)
print json_result
illust = json_result.response[0]
print ">>> %s, origin url: %s" % (illust.caption, illust.image_urls['large'])

# 用户资料 PAPI.users
json_result = api.users(1184799)
print json_result
user = json_result.response[0]
print user.profile.introduction

# 我的订阅 PAPI.me_feeds
json_result = api.me_feeds(show_r18=0)
print json_result
ref_work = json_result.response[0].ref_work
print ref_work.title

# 用户作品 PAPI.users_works
json_result = api.users_works(1184799)
print json_result
illust = json_result.response[0]
print ">>> %s, origin url: %s" % (illust.caption, illust.image_urls['large'])

# 用户收藏 PAPI.users_favorite_works
json_result = api.users_favorite_works(1184799)
print json_result
illust = json_result.response[0].work
print ">>> %s origin url: %s" % (illust.caption, illust.image_urls['large'])

# 排行榜 PAPI.ranking_all
json_result = api.ranking_all('weekly', 1)
print json_result
illust = json_result.response[0].works[0].work
print ">>> %s origin url: %s" % (illust.title, illust.image_urls['large'])

# 过去排行榜 PAPI.ranking_all(2015-05-01)
json_result = api.ranking_all(mode='daily', page=1, date='2015-05-01')
print json_result
illust = json_result.response[0].works[0].work
print ">>> %s origin url: %s" % (illust.title, illust.image_urls['large'])

# 标签(exact_tag)/标题(text)搜索 PAPI.search_works
json_result = api.search_works("水遊び", page=1, mode='exact_tag')
print json_result
illust = json_result.response[0]
print ">>> %s origin url: %s" % (illust.title, illust.image_urls['large'])
~~~

## License

Feel free to use, reuse and abuse the code in this project.
