# -*- coding:utf-8 -*-

import json

class Pixiv_PAPI(object):

	def __init__(self, api):
		self.api = api

	def _bearer_token(self):
		# return Android Bearer Key
		return 'Bearer %s' % '8mMXXWT9iuwdJvsVIvQsFYDwuZpRCMePeyagSh30ZdU'

	def get_works(self, illust_id):
		""" get full illust data """
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

		try:
			result = self.api._parse_json(r.text)
			return result
		except Exception, e:
			raise PixivError("parse_json() error: %s" % (e), header=r.headers, body=r.text)

