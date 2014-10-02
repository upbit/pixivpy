# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Pixiv API

from csv import reader
from .compat import StringIO, urlencode, py2, text
from datetime import datetime

if py2:
	# FIX BUG: csv.reader(StringIO(data)) only work on UTF-8 encode in Python2.7
	import sys
	reload(sys)
	sys.setdefaultencoding('utf-8')

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


def kv_populate(obj, keys, alias, values):
	for k, a, v in zip(keys, alias, values):
		if k:
			val = cast(v, k[1], k[2])
			setattr(obj, k[0], val)
			# add alias for key
			if isinstance(a, (list, tuple)):
				[ setattr(obj, k2a, val) for k2a in a if k2a ]
			elif a:		# not None
				setattr(obj, a, val)


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
		return [kv_populate(self.model(*args, **kwargs), self.keys, self.alias, row) for row in csv(data)]


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

	# Add image / page URL and alias
	@property
	def image_url(self):
		base = self.image_480mw[0:self.image_480mw.rfind("/mobile/")+1]
		return "%s%s.%s" % (base, self.illust_id, self.type)
	@property
	def imageURL(self):
		return self.image_url

	@property
	def page_url(self):
		base = self.image_480mw[0:self.image_480mw.rfind("/mobile/")+1]
		result = []
		if (self.pages > 0):
			for i in range(self.pages):
				result.append("%s%s_big_p%d.%s" % (base, self.illust_id, i, self.type))
		else:
			result.append(self.image_url)
		return result
	@property
	def pageURL(self):
		return self.page_url

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

	# from http://sourceforge.jp/projects/pxv/scm/svn/blobs/head/trunk/src/pxv/Image.java
	# illust_id, id, type, title, server, name, thumbnail,,, mobile,,, date, tags, use_tool, ranking, total, views, description,,,, unknow1, unknow2, user_name,, unknow3,,, head,
	# Image property aliases
	alias = (
		("id"),
		("author_id", "authorId"),
		("ext"),
		(None),		# title
		("server"),
		("author_name", "authorName"),
		("thumbnail", "thumbURL"),
		None,
		None,
		("mobile", "mobileURL"),
		None,
		None,
		(None),		# data
		(None),		# tags
		("use_tool"),
		("feedback"),
		("point"),
		("views"),
		("comment"),
		("pages"),
		None,
		None,
		("bookmarks"),
		(None),		# cnt_comment
		("username"),
		None,
		("isR18"),		# r18
		None,
		None,
		("head"),
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
	# User property aliases
	alias = (
		None,
		("author_id", "authorId"),
		None, None, None,
		("author_name", "authorName"),
		("thumbnail", "thumbURL"),
		None, None, None,
		None, None, None,
		None, None, None,
		None, None, None,
		None, None, None,
		None, None,
		("user_name", "username"),
		None,
	)
