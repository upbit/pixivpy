PixivPy
======
_Pixiv API for Python (with Auth supported)_

* [2014/10/07] new framework, **SAPI / Public-API** supported (requests needed)

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

### Authentication required! call api.login first!
print(">>> sapi.get_bookmark(1418182, page=1)")
bookmark_list = api.sapi.get_bookmark(1418182)
for img in bookmark_list:
	print(img)
~~~~~

### About

1. Blog: [Pixiv Public-API (OAuth)分析](http://blog.imaou.com/opensource/2014/10/09/pixiv_api_for_ios_update.html)

If you have any questions, please feel free to contact me: rmusique@gmail.com

Find Pixiv API in **Objective-C**? You might also like [**PixivAPI_iOS**](https://github.com/upbit/PixivAPI_iOS)

## API functions

### SAPI

[api.sapi](https://github.com/upbit/pixivpy/blob/master/pixivpy2/sapi.py).*

~~~~~ python
class Pixiv_SAPI(object):

	# 每日排行
	# content: [all, male, female, original]
	# mode: [day, week, month]
	# p: [1-n]
	def ranking(self, content='all', mode='day', p=1):

	# 过去的排行
	# Date_Year: 2014
	# Date_Month: 04
	# Date_Day: 01
	# mode: [daily, weekly, monthly, male, female, rookie]
	#       require_auth[daily_r18, weekly_r18, male_r18, female_r18, r18g]
	# p: [1-n]
	def ranking_log(self, Date_Year, Date_Month, Date_Day,
									mode="weekly", p=1, require_auth=False):

	# 作品信息 (新版客户端已使用 PAPI/works 代替)
	# require_auth - 获取r18作品信息时需要带登录信息
	@deprecated
	def get_illust(self, illust_id, require_auth=False):

	# 用户作品列表
	# id: author id
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

	# 用户收藏
	def users_favorite_works(self, author_id, page=1, per_page=30):
~~~~~

## License

Feel free to use, reuse and abuse the code in this project.
