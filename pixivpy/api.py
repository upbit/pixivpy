# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .compat import *

# Pixiv API
# modify from tweepy (https://github.com/tweepy/tweepy/)

from pixivpy.binder import bind_api
from pixivpy.parsers import ImageParser, UserParser


class PixivAPI(object):
	def __init__(self, host="spapi.pixiv.net", port=80, compression=True, timeout=60):
		self.api_root = "http://spapi.pixiv.net/iphone/"
		self.host = host
		self.port = port
		self.compression = compression
		self.timeout = timeout
		self.session = None

	def set_session(self, PHPSESSID):
		"""Pixiv PHPSESSID expires in one hour"""
		self.session = PHPSESSID
		return self.session

	# WARNNING: login API no longer exists, it return 404 Not Found
	login = bind_api(
		save_session = True,
		path = 'login.php',
		allowed_param = ['mode','pixiv_id','pass','skip'],
	)

	# get PHPSESSID from www.pixiv.net
	def login2(self, username, password):
		url = "http://www.pixiv.net/login.php"
		host, port = "www.pixiv.net", 80
		conn = HTTPConnection(host, port, timeout=30)

		headers = {}
		
		headers['Accept-encoding'] = 'gzip'
		headers['Origin'] = 'www.pixiv.net'
		headers['Referer'] = 'http://www.pixiv.net/login.php'
		headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
		# Important!
		headers['Content-Type'] = 'application/x-www-form-urlencoded'

		parameters = []
		parameters.append(('mode', 'login'))
		parameters.append(('return_to', '/'))
		parameters.append(('pixiv_id', username))
		parameters.append(('pass', password))
		
		post_data = urlencode(parameters)

		try:
			conn.request("POST", url, post_data, headers)
			resp = conn.getresponse()
		except Exception as e:
			raise Exception('Failed to send request: %s' % e)
		else:
			body = resp.read()
		finally:
			conn.close()

		if resp.status in (200,301,302,):
			redirect_url = resp.getheader('location', '')
			if resp.getheader('Set-Cookie'):
				session_string = resp.getheader('Set-Cookie').split(';')[0]
				self.session = session_string.split('=')[1].strip()
			else:
				self.session = redirect_url[redirect_url.rfind("PHPSESSID")+len("PHPSESSID")+1:]
			return self.session

		if resp.getheader('Content-Encoding', '') == 'gzip':
			try:
				zipper = gzip.GzipFile(fileobj=BytesIO(body))
				body = zipper.read()
			except Exception as e:
				raise Exception('Failed to decompress data: %s' % e)

		raise Exception('Unknow HTTP error: %d\n%s' % (resp.status, body))

	# content: [all, male, female, original]
	# mode: [day, week, month]
	# p: [1-n]
	ranking = bind_api(
		path = 'ranking.php',
		allowed_param = ['content','mode','p'],
		parser = ImageParser(),
		payload_list = True,
	)

	# Date_Year: 2013
	# Date_Month: 01
	# Date_Day: 01
	# mode: [daily, weekly, monthly, male, female]
	# p: [1-n]
	ranking_log = bind_api(
		path = 'ranking_log.php',
		allowed_param = ['Date_Year','p','mode','Date_Month','Date_Day'],
		parser = ImageParser(),
		payload_list = True,
	)

	get_illust = bind_api(
		path = 'illust.php',
		allowed_param = ['illust_id'],
		parser = ImageParser(),
	)

	get_member = bind_api(
		path = 'member_illust.php',
		allowed_param = ['id','p'],
		parser = ImageParser(),
		payload_list = True,
	)
	
	get_bookmark = bind_api(
		path = 'bookmark.php',
		allowed_param = ['id','p'],
		require_auth = True,				# auto parse PHPSESSID in url
		parser = ImageParser(),
		payload_list = True,
	)

	# level: 3
	get_user = bind_api(
		path = 'user.php',
		allowed_param = ['level','user_id'],
		parser = UserParser(),
	)

	# id: authorId
	# p: [1-n]
	get_mypixiv_all = bind_api(
		path = 'mypixiv_all.php',
		allowed_param = ['id','p'],
		parser = UserParser(),
		payload_list = True,
	)
