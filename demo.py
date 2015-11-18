#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
if sys.version_info >= (3, 0):
	import imp
	imp.reload(sys)
else:
	reload(sys)
	sys.setdefaultencoding('utf8')
sys.dont_write_bytecode = True

from pixivpy3 import *

### change _USERNAME,_PASSWORD first!
_USERNAME = "usersp"
_PASSWORD = "passsp"

def migrate_rev2_to_papi(api):
	print(">>> new ranking_all(mode='daily', page=1, per_page=50)")
	#rank_list = api.sapi.ranking("all", 'day', 1)
	rank_list = api.ranking_all('daily', 1, 50)
	print(rank_list)

	# more fields about response: https://github.com/upbit/pixivpy/wiki/sniffer
	ranking = rank_list.response[0]
	for img in ranking.works:
		#print img.work
		print("[%s/%s(id=%s)] %s" % (img.work.user.name, img.work.title, img.work.id, img.work.image_urls.px_480mw))

def papi_demo(api):
	# PAPI.works
	json_result = api.works(46363414)
	print(json_result)
	illust = json_result.response[0]
	print(">>> %s, origin url: %s" % (illust.caption, illust.image_urls['large']))

	# PAPI.users
	json_result = api.users(1184799)
	print(json_result)
	user = json_result.response[0]
	print(user.profile.introduction)

	# PAPI.me_feeds
	json_result = api.me_feeds(show_r18=0)
	print(json_result)
	ref_work = json_result.response[0].ref_work
	print(ref_work.title)

	# PAPI.users_works
	json_result = api.users_works(1184799)
	print(json_result)
	illust = json_result.response[0]
	print(">>> %s, origin url: %s" % (illust.caption, illust.image_urls['large']))

	# PAPI.users_favorite_works
	json_result = api.users_favorite_works(1184799)
	print(json_result)
	illust = json_result.response[0].work
	print(">>> %s origin url: %s" % (illust.caption, illust.image_urls['large']))

	# PAPI.ranking_all
	json_result = api.ranking_all('weekly', 1)
	print(json_result)
	illust = json_result.response[0].works[0].work
	print(">>> %s origin url: %s" % (illust.title, illust.image_urls['large']))

	# PAPI.ranking_all(2015-05-01)
	json_result = api.ranking_all(mode='daily', page=1, date='2015-05-01')
	print(json_result)
	illust = json_result.response[0].works[0].work
	print(">>> %s origin url: %s" % (illust.title, illust.image_urls['large']))

	# PAPI.search_works
	json_result = api.search_works("五航戦 姉妹", page=1, mode='text')
	#json_result = api.search_works("水遊び", page=1, mode='exact_tag')
	print(json_result)
	illust = json_result.response[0]
	print(">>> %s origin url: %s" % (illust.title, illust.image_urls['large']))

def refresh_token(api):
	"""
	Acquire a new bearer token after your current token expires,
	  just call auth() or specifies a refresh_token
	"""

	print("refresh_token before: %s" % api.refresh_token)

	# api.auth(refresh_token = api.refresh_token)
	api.auth()

	print("refresh_token  after: %s" % api.refresh_token)

def main():
	api = PixivAPI()
	api.login(_USERNAME, _PASSWORD)

	#migrate_rev2_to_papi(api)
	papi_demo(api)

	refresh_token(api)

if __name__ == '__main__':
	main()
