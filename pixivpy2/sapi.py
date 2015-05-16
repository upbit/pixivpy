# -*- coding:utf-8 -*-

import json

from sapi_parsers import ImageParser, UserParser

class Pixiv_SAPI(object):

	def __init__(self, api):
		self.api = api
		self.api_root = ''

	def parser_payload(self, data, parser, payload_list=False):
		result = parser(data)
		if not payload_list:
			result = result[0] if len(result) else None
		return result

	# 每日排行 (新版客户端已使用 PAPI/ranking_all 代替)
	# content: [all, male, female, original]
	# mode: [day, week, month]
	# p: [1-n]
	def ranking(self, content='all', mode='day', p=1):
		url = 'http://spapi.pixiv.net/iphone/ranking.php'
		params = {
			'content': content,
			'mode': mode,
			'p': p,
		}
		r = self.api._requests_call('GET', url, params=params)
		return self.parser_payload(r.text, ImageParser(), payload_list=True)

	# 过去的排行 (新版客户端已使用 PAPI/ranking_all 代替)
	# Date_Year: 2014
	# Date_Month: 04
	# Date_Day: 01
	# mode: [daily, weekly, monthly, male, female, rookie], require_auth[daily_r18, weekly_r18, male_r18, female_r18, r18g]
	# p: [1-n]
	def ranking_log(self, Date_Year, Date_Month, Date_Day, mode="weekly", p=1, require_auth=False):
		url = 'http://spapi.pixiv.net/iphone/ranking_log.php'
		params = {
			'Date_Year': Date_Year,
			'Date_Month': Date_Month,
			'Date_Day': Date_Day,
			'mode': mode,
			'p': p,
		}
		if require_auth:
			self.api._require_auth()
			params['PHPSESSID'] = self.api.session

		r = self.api._requests_call('GET', url, params=params)
		return self.parser_payload(r.text, ImageParser(), payload_list=True)

	# 作品信息 (新版客户端已使用 PAPI/works 代替)
	# require_auth - 获取r18作品信息时需要带登录信息
	def get_illust(self, illust_id, require_auth=False):
		url = 'http://spapi.pixiv.net/iphone/illust.php'
		headers = {
			'User-Agent': 'pixiv-ios-app(ver4.0.0)',
		}
		params = {
			'illust_id': illust_id,
		}
		if require_auth:
			self.api._require_auth()
			params['PHPSESSID'] = self.api.session

		r = self.api._requests_call('GET', url, params=params, headers=headers)
		return self.parser_payload(r.text, ImageParser())

	# 用户作品列表
	# id: author id
	def get_member(self, id, p=1):
		url = 'http://spapi.pixiv.net/iphone/member_illust.php'
		params = {
			'id': id,
			'p': p,
		}
		r = self.api._requests_call('GET', url, params=params)
		return self.parser_payload(r.text, ImageParser(), payload_list=True)

	# [需鉴权]用户收藏 (新版客户端已使用 PAPI/users/favorite_works 代替)
	def get_bookmark(self, id, p=1):
		self.api._require_auth()
		url = 'http://spapi.pixiv.net/iphone/bookmark.php'
		params = {
			'id': id,
			'p': p,
			'PHPSESSID': self.api.session,
		}
		r = self.api._requests_call('GET', url, params=params)
		return self.parser_payload(r.text, ImageParser(), payload_list=True)

	# 用户资料 (新版客户端已使用 PAPI/users 代替)
	# level: 3
	def get_user(self, user_id, level=3, require_auth=False):
		url = 'http://spapi.pixiv.net/iphone/user.php'
		headers = {
			'User-Agent': 'pixiv-ios-app(ver4.0.0)',
		}
		params = {
			'user_id': user_id,
			'level': level,
		}
		if require_auth:
			self.api._require_auth()
			params['PHPSESSID'] = self.api.session

		r = self.api._requests_call('GET', url, params=params, headers=headers)
		return self.parser_payload(r.text, UserParser())

	# 标记书签的用户
	# illust_id: target illust
	# p: page
	def get_illust_bookmarks(self, illust_id, p):
		url = 'http://spapi.pixiv.net/iphone/illust_bookmarks.php'
		params = {
			'illust_id': illust_id,
			'p': p,
		}
		r = self.api._requests_call('GET', url, params=params)
		return self.parser_payload(r.text, UserParser(), payload_list=True)

	# [需鉴权]关注
	# id: author id
	# p: [1-n]
	# rest: "show"
	def get_bookmark_user_all(self, id, p=1, rest="show"):
		self.api._require_auth()
		url = 'http://spapi.pixiv.net/iphone/bookmark_user_all.php'
		params = {
			'id': id,
			'p': p,
			'rest': rest,
			'PHPSESSID': self.api.session,
		}
		r = self.api._requests_call('GET', url, params=params)
		return self.parser_payload(r.text, UserParser(), payload_list=True)

	# 好P友
	# id: authorId
	# p: [1-n]
	def get_mypixiv_all(self, id, p):
		url = 'http://spapi.pixiv.net/iphone/mypixiv_all.php'
		params = {
			'id': id,
			'p': p,
		}
		r = self.api._requests_call('GET', url, params=params)
		return self.parser_payload(r.text, UserParser(), payload_list=True)
