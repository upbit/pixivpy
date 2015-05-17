# -*- coding:utf-8 -*-

from utils import PixivError

# [需鉴权]
class Pixiv_PAPI(object):

	def __init__(self, api):
		self.api = api

	def parse_result(self, req):
		try:
			return self.api._parse_json(req.text)
		except Exception, e:
			raise PixivError("parse_json() error: %s" % (e), header=req.headers, body=req.text)

	def bad_words(self):
		self.api._require_auth()

		url = 'https://public-api.secure.pixiv.net/v1.1/bad_words.json'
		headers = {
			'Authorization': 'Bearer %s' % self.api.access_token,
			'Cookie': 'PHPSESSID=%s' % self.api.session,
		}

		r = self.api._requests_call('GET', url, headers=headers)
		return self.parse_result(r)

	# 作品详细
	def works(self, illust_id):
		self.api._require_auth()

		url = 'https://public-api.secure.pixiv.net/v1/works/%d.json' % (illust_id)
		headers = {
			'Authorization': 'Bearer %s' % self.api.access_token,
			'Cookie': 'PHPSESSID=%s' % self.api.session,
		}
		params = {
			'profile_image_sizes': 'px_170x170,px_50x50',
			'image_sizes': 'px_128x128,small,medium,large,px_480mw',
			'include_stats': 'true',
		}

		r = self.api._requests_call('GET', url, headers=headers, params=params)
		return self.parse_result(r)

	# 用户资料
	def users(self, author_id):
		self.api._require_auth()

		url = 'https://public-api.secure.pixiv.net/v1/users/%d.json' % (author_id)
		headers = {
			'Authorization': 'Bearer %s' % self.api.access_token,
			'Cookie': 'PHPSESSID=%s' % self.api.session,
		}
		params = {
			'profile_image_sizes': 'px_170x170,px_50x50',
			'image_sizes': 'px_128x128,small,medium,large,px_480mw',
			'include_stats': 1,
			'include_profile': 1,
			'include_workspace': 1,
			'include_contacts': 1,
		}

		r = self.api._requests_call('GET', url, headers=headers, params=params)
		return self.parse_result(r)

	# 我的订阅
	def me_feeds(self, show_r18=1):
		self.api._require_auth()

		url = 'https://public-api.secure.pixiv.net/v1/me/feeds.json'
		headers = {
			'Authorization': 'Bearer %s' % self.api.access_token,
		}
		params = {
			'relation': 'all',
			'type': 'touch_nottext',
			'show_r18': show_r18,
		}

		r = self.api._requests_call('GET', url, headers=headers, params=params)
		return self.parse_result(r)

	# 用户作品列表
	# publicity:  public, private
	def users_works(self, author_id, page=1, per_page=30, publicity='public',
			image_sizes=['px_128x128', 'px_480mw', 'large'],
			profile_image_sizes=['px_170x170', 'px_50x50'],
			include_stats=True, include_sanity_level=True):
		self.api._require_auth()

		url = 'https://public-api.secure.pixiv.net/v1/users/%d/works.json' % (author_id)
		headers = {
			'Authorization': 'Bearer %s' % self.api.access_token,
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
		r = self.api._requests_call('GET', url, headers=headers, params=params)
		return self.parse_result(r)

	# 用户收藏
	# publicity:  public, private
	def users_favorite_works(self, author_id, page=1, per_page=30, publicity='public',
			image_sizes=['px_128x128', 'px_480mw', 'large'],
			profile_image_sizes=['px_170x170', 'px_50x50'],
			include_stats=True, include_sanity_level=True):
		self.api._require_auth()

		url = 'https://public-api.secure.pixiv.net/v1/users/%d/favorite_works.json' % (author_id)
		headers = {
			'Authorization': 'Bearer %s' % self.api.access_token,
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

		r = self.api._requests_call('GET', url, headers=headers, params=params)
		return self.parse_result(r)

	# 排行榜/过去排行榜
	# mode: [daily, weekly, monthly, male, female, rookie, daily_r18, weekly_r18, male_r18, female_r18, r18g]
	# page: [1-n]
	# date: '2015-04-01' (仅过去排行榜)
	def ranking_all(self, mode='daily', page=1, per_page=50, date=None,
			image_sizes=['px_128x128', 'px_480mw', 'large'],
			profile_image_sizes=['px_170x170', 'px_50x50'],
			include_stats=True, include_sanity_level=True):
		self.api._require_auth()

		url = 'https://public-api.secure.pixiv.net/v1/ranking/all'
		headers = {
			'Authorization': 'Bearer %s' % self.api.access_token,
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

		r = self.api._requests_call('GET', url, headers=headers, params=params)
		return self.parse_result(r)
