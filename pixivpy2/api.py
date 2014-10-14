# -*- coding:utf-8 -*-

import json
import requests

from papi import Pixiv_PAPI
from sapi import Pixiv_SAPI
from utils import PixivError, JsonDict

class PixivAPI(object):
	session = None
	access_token = None
	user_id = 0

	def __init__(self):
		self.sapi = Pixiv_SAPI(self)
		self.papi = Pixiv_PAPI(self)

	def _requests_call(self, method, url, headers={}, params=None, data=None):
		""" requests http/https call for Pixiv API """

		req_header = {
			'Referer': 'http://spapi.pixiv.net/',
			'User-Agent': 'PixivIOSApp/5.1.1',
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

