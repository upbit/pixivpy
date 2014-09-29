# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Pixiv API

from csv import reader
from .compat import StringIO, urlencode, py2, text
from datetime import datetime

def s2dt(string):
	return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")


def s2bool(string):
	return bool(int(string))


def cast(data, cb, default=None):
	if not data:
		return default
	elif callable(cb):
		try:
			return cb(data)
		except:
			return default
	else:
		return data


def kv_populate(obj, keys, values):
	for k, v in zip(keys, values):
		if k:
			setattr(obj, k[0], cast(v, k[1], k[2]))

	return obj


def csv(data):
	if not data:
		return
		yield

	for row in reader(StringIO(data)):
		yield row


class Parser(object):
	model = object
	keys = ()

	def __call__(self, data, *args, **kwargs):
		obj = self.model(*args, **kwargs)
		return [kv_populate(obj, self.keys, row) for row in csv(data)]


class Image(object):
	illust_id = 0
	r18 = False
	pages = 0
	date = datetime.utcnow()
	title = None
	tags = None
	tool = None
	description = None

	user_id = 0
	user_dispname = None
	user_name = None
	user_pic = None

	image_type = None
	image_server = 0
	image_128 = None
	image_480mw = None

	cnt_rated = 0
	cnt_score = 0
	cnt_view = 0
	cnt_bookmark = 0
	cnt_comment = 0

	@property
	def url(self):
		base = 'http://www.pixiv.net/member_illust.php'
		params = urlencode((('mode', 'medium'), ('illust_id', self.illust_id)))
		return '?'.join((base, params))

	def __repr__(self):
		fmt = (self.__class__.__name__, self.illust_id, self.title)
		return '<%s(%s) "%s">' % fmt


class ImageParser(Parser):
	model = Image
	keys = (
		("illust_id",     int,    0),
		("user_id",       int,    0),
		("type",          text,   None),
		("title",         text,   None),
		("image_server",  int,    1),
		("user_dispname", text,  None),
		("image_128",     text,  None),
		None,
		None,
		("image_480mw",   text,   None),
		None,
		None,
		("date",          s2dt,   None),
		("tags",          text,   None),
		("tool",          text,   None),
		("cnt_rated",     int,    0),
		("cnt_score",     int,    0),
		("cnt_view",      int,    0),
		("description",   text,   None),
		("pages",         int,    0),
		None,
		None,
		("cnt_bookmark",  int,    0),
		("cnt_comment",   int,    0),
		("user_name",     text,   None),
		None,
		("r18",           s2bool, False),
		None,
		None,
		("user_pic",      text,   None),
		None,
	)


class User(object):
	uid = 0
	dispname = None
	name = None
	pic = None

	@property
	def url(self):
		base = 'http://www.pixiv.net/member.php'
		params = urlencode({'id': self.uid})
		return '?'.join((base, params))

	def __repr__(self):
		class_name = self.__class__.__name__
		fmt = (class_name, self.uid, repr(self.name), self.dispname)
		return '<%s(%s, %s) "%s">' % fmt


class UserParser(Parser):
	model = User
	keys = (
		None,
		("uid",      int,  0),
		None, None, None,
		("dispname", text, None),
		("pic",      text, None),
		None, None, None,
		None, None, None,
		None, None, None,
		None, None, None,
		None, None, None,
		None, None,
		("name",     text, None),
		None,
	)
