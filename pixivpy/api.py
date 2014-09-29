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
