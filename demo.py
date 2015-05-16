#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

from pixivpy2 import *

_USERNAME = "username"
_PASSWORD = "password"

# def sapi_demo(api):
# 	print(">>> ranking(male, day, page=1)")
# 	rank_list = api.sapi.ranking("all", 'day', 1)
# 	for img in rank_list:
# 		print(img)

# 	illust = api.sapi.get_illust(46363414)
# 	print(">>> [%s] %s: %s" % (illust.authorName, illust.title, illust.url))

# 	print(">>> get_user(id=1184799, level=3)")
# 	user = api.sapi.get_user(1184799, level=3)
# 	print("%s: %s" % (user.author_name, user.thumbURL))

# 	## Authentication required! call api.login first!
# 	print(">>> sapi.get_bookmark(1418182, page=1)")
# 	bookmark_list = api.sapi.get_bookmark(1418182)
# 	for img in bookmark_list:
# 		print(img)

def migrate_sapi_to_papi(api):
	print(">>> new ranking_all(mode='daily', page=1, per_page=50)")
	#rank_list = api.sapi.ranking("all", 'day', 1)
	rank_list = api.papi.ranking_all('daily', 1, 50)
	#rank_list = api.papi.ranking_all('weekly', 1, 50, date='2015-05-01')		# ranking log: weekly, 2015-05-01
	print rank_list

	# more fields about response: https://github.com/upbit/pixivpy/wiki/sniffer
	ranking = rank_list.response[0]
	for img in ranking.works:
		#print img.work
		print "[%s/%s(id=%s)] %s" % (img.work.user.name, img.work.title, img.work.id, img.work.image_urls.px_480mw)

def papi_demo(api):
	json_result = api.papi.works(46363414)
	print json_result
	illust = json_result.response[0]
	print ">>> origin url: %s" % illust.image_urls['large']

	#json_result = api.papi.users(1184799)
	#print json_result
	#user = json_result.response[0]
	#print user.profile.introduction

def main():
	api = PixivAPI()

	### change _USERNAME,_PASSWORD first!
	api.login(_USERNAME, _PASSWORD)

	migrate_sapi_to_papi(api)
	#papi_demo(api)

if __name__ == '__main__':
	main()
