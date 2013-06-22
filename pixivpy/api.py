# Pixiv API
# modify from tweepy (https://github.com/tweepy/tweepy/)

from pixivpy.binder import bind_api
from pixivpy.parsers import ImageParser

class PixivAPI(object):
	def __init__(self, host="spapi.pixiv.net", port=80, compression=True, timeout=60):
		self.api_root = "http://spapi.pixiv.net/iphone/"
		self.host = host
		self.port = port
		self.compression = compression
		self.timeout = timeout
		self.session = None

	login = bind_api(
		save_session = True,
		path = 'login.php',
		allowed_param = ['mode','pixiv_id','pass','skip'],
	)

	ranking = bind_api(
		path = 'ranking.php',
		allowed_param = ['content','mode','p'],
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
