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

	# Date_Year: 2013
	# Date_Month: 01
	# Date_Day: 01
	# mode: [daily, weekly, monthly, male, female]
	# p: [1-n]
	def ranking_log(self, Date_Year, Date_Month, Date_Day, mode="weekly", p=1):
		url = 'http://spapi.pixiv.net/iphone/ranking_log.php'
		params = {
			'Date_Year': Date_Year,
			'Date_Month': Date_Month,
			'Date_Day': Date_Day,
			'mode': mode,
			'p': p,
		}
		r = self.api._requests_call('GET', url, params=params)
		return self.parser_payload(r.text, ImageParser(), payload_list=True)

	def get_illust(self, illust_id):
		url = 'http://spapi.pixiv.net/iphone/illust.php'
		headers = {
			'User-Agent': 'pixiv-ios-app(ver4.0.0)',
		}
		params = {
			'illust_id': illust_id,
		}
		r = self.api._requests_call('GET', url, params=params, headers=headers)
		return self.parser_payload(r.text, ImageParser())

	def get_member(self, id, p=1):
		url = 'http://spapi.pixiv.net/iphone/member_illust.php'
		params = {
			'id': id,
			'p': p,
		}
		r = self.api._requests_call('GET', url, params=params)
		return self.parser_payload(r.text, ImageParser(), payload_list=True)

	def get_bookmark(self, id, p=1):
		self.api._require_auth()
		#url = 'http://httpbin.org/get'
		url = 'http://spapi.pixiv.net/iphone/bookmark.php'
		params = {
			'id': id,
			'p': p,
			'PHPSESSID': self.api.session,
		}
		r = self.api._requests_call('GET', url, params=params)
		return self.parser_payload(r.text, ImageParser(), payload_list=True)

	# level: 3
	def get_user(self, user_id, level=3):
		url = 'http://spapi.pixiv.net/iphone/user.php'
		headers = {
			'User-Agent': 'pixiv-ios-app(ver4.0.0)',
		}
		params = {
			'user_id': user_id,
			'level': level,
		}
		r = self.api._requests_call('GET', url, params=params, headers=headers)
		return self.parser_payload(r.text, UserParser())

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

	# id: authorId
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
