# -*- coding:utf-8 -*-

import json
import requests

from papi import Pixiv_PAPI
from sapi import Pixiv_SAPI

class PixivError(Exception):
	"""Pixiv API exception"""
	def __init__(self, reason, header=None, body=None):
		self.reason = unicode(reason)
		self.header = header
		self.body = body
		Exception.__init__(self, reason)
	def __str__(self):
		return self.reason

class JsonDict(dict):
	"""general json object that allows attributes to be bound to and also behaves like a dict"""
	def __getattr__(self, attr):
		try:
			return self[attr]
		except KeyError:
			raise AttributeError(r"'JsonDict' object has no attribute '%s'" % attr)
	def __setattr__(self, attr, value):
		self[attr] = value

class PixivAPI(object):
	session = None

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
		if (self.session == None):
			raise PixivError('Authentication required! Call login() or set_session() first!')

	def set_session(self, session_id):
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

		try:
			raw_cookie = r.headers.get('Set-Cookie')
			for cookie_str in raw_cookie.split('; '):
				if 'PHPSESSID=' in cookie_str:
					self.session = cookie_str.split('=')[1]
			print self.session
		except:
			raise PixivError('Get PHPSESSID error! Set-Cookie: %s' % (r.headers.get('Set-Cookie')), header=r.headers, body=r.text)

