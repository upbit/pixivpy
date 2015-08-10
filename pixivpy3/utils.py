# -*- coding:utf-8 -*-

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
