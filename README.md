PixivPy
======
_Pixiv API for Python (with Auth supported)_

* [2015/05/16] As Pixiv **deprecated** SAPI in recent days, push new Public-API **ranking_all**
* [2014/10/07] New framework, **SAPI / Public-API** supported (requests needed)

Requirements: [requests](https://pypi.python.org/pypi/requests), use pip to install:

~~~~
pip install requests
~~~~

### Example:

~~~~~ python
api = PixivAPI()
api.login("username", "password")

# get origin url
json_result = api.papi.get_works(45455208)
illust = json_result.response[0]
print "origin url: %s" % illust.image_urls['large']

# get ranking (page1)
json_result = api.papi.ranking_all('daily')
ranking = json_result.response[0]
for illust in ranking.works:
	print "[%s] %s" % (illust.work.title, illust.work.image_urls.px_480mw)
~~~~~

### About

1. Blog: [Pixiv Public-API (OAuth)分析](http://blog.imaou.com/opensource/2014/10/09/pixiv_api_for_ios_update.html)

If you have any questions, please feel free to contact me: rmusique@gmail.com

Find Pixiv API in **Objective-C**? You might also like [**PixivAPI_iOS**](https://github.com/upbit/PixivAPI_iOS)

## API functions

### Public-API

[api.papi](https://github.com/upbit/pixivpy/blob/master/pixivpy2/papi.py).*

~~~~~ python
# [需鉴权]
class Pixiv_PAPI(object):

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
~~~~~

### SAPI

[api.sapi](https://github.com/upbit/pixivpy/blob/master/pixivpy2/sapi.py).*

~~~~~ python
class Pixiv_SAPI(object):

	# 每日排行 (新版客户端已使用 PAPI/ranking_all 代替)
	# content: [all, male, female, original]
	# mode: [day, week, month]
	# p: [1-n]
	@deprecated
	def ranking(self, content='all', mode='day', p=1):

	# 过去的排行 (新版客户端已使用 PAPI/ranking_all 代替)
	# Date_Year: 2014
	# Date_Month: 04
	# Date_Day: 01
	# mode: [daily, weekly, monthly, male, female, rookie]
	#       require_auth[daily_r18, weekly_r18, male_r18, female_r18, r18g]
	# p: [1-n]
	@deprecated
	def ranking_log(self, Date_Year, Date_Month, Date_Day,
									mode="weekly", p=1, require_auth=False):

	# 作品信息 (新版客户端已使用 PAPI/works 代替)
	# require_auth - 获取r18作品信息时需要带登录信息
	@deprecated
	def get_illust(self, illust_id, require_auth=False):

	# 用户作品列表 (新版客户端已使用 PAPI/users_works 代替)
	# id: author id
	@deprecated
	def get_member(self, id, p=1):

	# [需鉴权]用户收藏 (新版客户端已使用 PAPI/users/favorite_works 代替)
	@deprecated
	def get_bookmark(self, id, p=1):

	# 用户资料 (新版客户端已使用 PAPI/users 代替)
	# level: 3
	@deprecated
	def get_user(self, user_id, level=3, require_auth=False):

	# 标记书签的用户
	# illust_id: target illust
	# p: page
	def get_illust_bookmarks(self, illust_id, p):

	# 关注
	# id: author id
	# p: [1-n]
	# rest: "show"
	def get_bookmark_user_all(self, id, p=1, rest="show"):

	# 好P友
	# id: authorId
	# p: [1-n]
	def get_mypixiv_all(self, id, p):
~~~~~

## License

Feel free to use, reuse and abuse the code in this project.
