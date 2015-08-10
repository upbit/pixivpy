# -*- coding:utf-8 -*-

import json
import requests

from utils import PixivError, JsonDict

class BasePixivAPI:
	session = None
	access_token = None
	user_id = 0

	def _requests_call(self, method, url, headers={}, params=None, data=None):
		""" requests http/https call for Pixiv API """

		req_header = {
			'Referer': 'http://spapi.pixiv.net/',
			'User-Agent': 'PixivIOSApp/5.6.0',
			'Content-Type': 'application/x-www-form-urlencoded',
		}
		# override use user headers
		for k,v in headers.items():
			req_header[k] = v

		try:
			if (method == 'GET'):
				return requests.get(url, params=params, headers=req_header)
			elif (method == 'POST'):
				return requests.post(url, params=params, data=data, headers=req_header)
		except Exception, e:
			raise PixivError('requests %s %s error: %s' % (method, url, e))

		raise PixivError('Unknow method: %s' % method)

	def _parse_json(self, json_str):
		"""parse str into JsonDict"""

		def _obj_hook(pairs):
			"""convert json object to python object"""
			o = JsonDict()
			for k, v in pairs.iteritems():
				o[str(k)] = v
			return o

		return json.loads(json_str, object_hook=_obj_hook)

	def _require_auth(self):
		if (self.access_token == None) or (self.session == None):
			raise PixivError('Authentication required! Call login() or set_auth() first!')

	def set_auth(self, access_token, session_id):
		self.access_token = access_token
		self.session = session_id

	def login(self, username, password):
		url = 'https://oauth.secure.pixiv.net/auth/token'
		headers = {
			'Referer': 'http://www.pixiv.net/',
		}
		data = {
			'username': username,
			'password': password,
			'grant_type': 'password',
			'client_id': 'bYGKuGVw91e0NMfPGp44euvGt59s',
			'client_secret': 'HP3RmkgAmEGro0gn1x9ioawQE8WMfvLXDz3ZqxpK',
		}

		r = self._requests_call('POST', url, headers=headers, data=data)
		if (not r.status_code in [200, 301, 302]):
			raise PixivError('[ERROR] login() failed! check username and password.\nHTTP %s: %s' % (r.status_code, r.text), header=r.headers, body=r.text)

		token = None
		try:
			# get access_token
			token = self._parse_json(r.text)
			self.access_token = token.response.access_token
			self.user_id = token.response.user.id
			print "AccessToken:", self.access_token

		except:
			raise PixivError('Get access_token error! Response: %s' % (token), header=r.headers, body=r.text)

		try:
			# get PHPSESSID
			raw_cookie = r.headers.get('Set-Cookie')
			for cookie_str in raw_cookie.split('; '):
				if 'PHPSESSID=' in cookie_str:
					self.session = cookie_str.split('=')[1]
			print "Session:", self.session

		except:
			raise PixivError('Get PHPSESSID error! Set-Cookie: %s' % (r.headers.get('Set-Cookie')), header=r.headers, body=r.text)

		# return auth/token response
		return token

## Public-API
class PixivAPI(BasePixivAPI):

	def parse_result(self, req):
		try:
			return self._parse_json(req.text)
		except Exception, e:
			raise PixivError("parse_json() error: %s" % (e), header=req.headers, body=req.text)

	def bad_words(self):
		self._require_auth()

		url = 'https://public-api.secure.pixiv.net/v1.1/bad_words.json'
		headers = {
			'Authorization': 'Bearer %s' % self.access_token,
			'Cookie': 'PHPSESSID=%s' % self.session,
		}

		r = self._requests_call('GET', url, headers=headers)
		return self.parse_result(r)

	# 作品详细
	def works(self, illust_id):
		self._require_auth()

		url = 'https://public-api.secure.pixiv.net/v1/works/%d.json' % (illust_id)
		headers = {
			'Authorization': 'Bearer %s' % self.access_token,
			'Cookie': 'PHPSESSID=%s' % self.session,
		}
		params = {
			'profile_image_sizes': 'px_170x170,px_50x50',
			'image_sizes': 'px_128x128,small,medium,large,px_480mw',
			'include_stats': 'true',
		}

		r = self._requests_call('GET', url, headers=headers, params=params)
		return self.parse_result(r)

	# 用户资料
	def users(self, author_id):
		self._require_auth()

		url = 'https://public-api.secure.pixiv.net/v1/users/%d.json' % (author_id)
		headers = {
			'Authorization': 'Bearer %s' % self.access_token,
			'Cookie': 'PHPSESSID=%s' % self.session,
		}
		params = {
			'profile_image_sizes': 'px_170x170,px_50x50',
			'image_sizes': 'px_128x128,small,medium,large,px_480mw',
			'include_stats': 1,
			'include_profile': 1,
			'include_workspace': 1,
			'include_contacts': 1,
		}

		r = self._requests_call('GET', url, headers=headers, params=params)
		return self.parse_result(r)

	# 我的订阅
	def me_feeds(self, show_r18=1):
		self._require_auth()

		url = 'https://public-api.secure.pixiv.net/v1/me/feeds.json'
		headers = {
			'Authorization': 'Bearer %s' % self.access_token,
		}
		params = {
			'relation': 'all',
			'type': 'touch_nottext',
			'show_r18': show_r18,
		}

		r = self._requests_call('GET', url, headers=headers, params=params)
		return self.parse_result(r)

	# 用户作品列表
	# publicity:  public, private
	def users_works(self, author_id, page=1, per_page=30, publicity='public',
			image_sizes=['px_128x128', 'px_480mw', 'large'],
			profile_image_sizes=['px_170x170', 'px_50x50'],
			include_stats=True, include_sanity_level=True):
		self._require_auth()

		url = 'https://public-api.secure.pixiv.net/v1/users/%d/works.json' % (author_id)
		headers = {
			'Authorization': 'Bearer %s' % self.access_token,
		}
		params = {
			'page': page,
			'per_page': per_page,
			'publicity': publicity,
			'include_stats': include_stats,
			'include_sanity_level': include_sanity_level,
			'image_sizes': ','.join(image_sizes),
			'profile_image_sizes': ','.join(profile_image_sizes),
		}
		
		r = self._requests_call('GET', url, headers=headers, params=params)
		return self.parse_result(r)

	# 用户收藏
	# publicity:  public, private
	def users_favorite_works(self, author_id, page=1, per_page=30, publicity='public',
			image_sizes=['px_128x128', 'px_480mw', 'large'],
			profile_image_sizes=['px_170x170', 'px_50x50'],
			include_stats=True, include_sanity_level=True):
		self._require_auth()

		url = 'https://public-api.secure.pixiv.net/v1/users/%d/favorite_works.json' % (author_id)
		headers = {
			'Authorization': 'Bearer %s' % self.access_token,
		}
		params = {
			'page': page,
			'per_page': per_page,
			'publicity': publicity,
			'include_stats': include_stats,
			'include_sanity_level': include_sanity_level,
			'image_sizes': ','.join(image_sizes),
			'profile_image_sizes': ','.join(profile_image_sizes),
		}

		r = self._requests_call('GET', url, headers=headers, params=params)
		return self.parse_result(r)

	# 排行榜/过去排行榜
	# mode: [daily, weekly, monthly, male, female, rookie, daily_r18, weekly_r18, male_r18, female_r18, r18g]
	# page: [1-n]
	# date: '2015-04-01' (仅过去排行榜)
	def ranking_all(self, mode='daily', page=1, per_page=50, date=None,
			image_sizes=['px_128x128', 'px_480mw', 'large'],
			profile_image_sizes=['px_170x170', 'px_50x50'],
			include_stats=True, include_sanity_level=True):
		self._require_auth()

		url = 'https://public-api.secure.pixiv.net/v1/ranking/all'
		headers = {
			'Authorization': 'Bearer %s' % self.access_token,
		}
		params = {
			'mode': mode,
			'page': page,
			'per_page': per_page,
			'include_stats': include_stats,
			'include_sanity_level': include_sanity_level,
			'image_sizes': ','.join(image_sizes),
			'profile_image_sizes': ','.join(profile_image_sizes),
		}
		if date:	# 过去排行榜
			params['date'] = date

		r = self._requests_call('GET', url, headers=headers, params=params)
		return self.parse_result(r)
