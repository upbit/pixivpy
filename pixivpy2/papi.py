# -*- coding:utf-8 -*-

import json

class Pixiv_PAPI(object):

	def __init__(self, api):
		self.api = api

	def _bearer_token(self):
		# return Android Bearer Key
		return 'Bearer %s' % '8mMXXWT9iuwdJvsVIvQsFYDwuZpRCMePeyagSh30ZdU'

	def parse_result(self, req):
		try:
			return self.api._parse_json(req.text)
		except Exception, e:
			raise PixivError("parse_json() error: %s" % (e), header=req.headers, body=req.text)


	def works(self, illust_id):
		self.api._require_auth()

		url = 'https://public-api.secure.pixiv.net/v1/works/%d.json' % (illust_id)
		headers = {
			'Authorization': self._bearer_token(),
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
			'Authorization': self._bearer_token(),
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
