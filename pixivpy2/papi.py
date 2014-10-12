# -*- coding:utf-8 -*-

from utils import PixivError

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


	def me_feeds(self, show_r18=1):
		self.api._require_auth()

		url = 'https://public-api.secure.pixiv.net/v1/me/feeds.json'
		headers = {
			'Authorization': 'Bearer %s' % self.api.access_token,
			'Cookie': 'PHPSESSID=%s' % self.api.session,
		}
		params = {
			'relation': 'all',
			'type': 'touch_nottext',
			'show_r18': show_r18,
		}

		r = self.api._requests_call('GET', url, headers=headers, params=params)
		return self.parse_result(r)

	def users_favorite_works(self, author_id, page=1, per_page=30):
		self.api._require_auth()

		url = 'https://public-api.secure.pixiv.net/v1/users/%d/favorite_works.json' % (author_id)
		headers = {
			'Authorization': 'Bearer %s' % self.api.access_token,
			'Cookie': 'PHPSESSID=%s' % self.api.session,
		}
		params = {
			'page': page,
			'per_page': per_page,
			'publicity': 'public',								# public or private
			'include_work': 'true',
			'include_stats': 'true',
			'image_sizes': 'px_128x128,small,medium,large,px_480mw',
			'profile_image_sizes': 'px_170x170,px_50x50',
		}

		r = self.api._requests_call('GET', url, headers=headers, params=params)
		return self.parse_result(r)



