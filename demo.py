#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pixivpy import *

_USERNAME = "username"
_PASSWORD = "password"

def main():
	api = PixivAPI()
	#api = PixivAPI(host="127.0.0.1", port=8888)    # for proxy

	### change _USERNAME,_PASSWORD first!
	#api.login("login", _USERNAME, _PASSWORD, 0)

	#print ">>> ranking(male, day, page=1)"
	#rank_list = api.ranking("all", 'day', 1)
	#for img in rank_list:
	#	print img

	#illust = api.get_illust(36503804)
	#print ">>> %d %s" % (illust.authorId, illust.mobileURL)

	#print ">>> get_member(176223, page=1)"
	#illust_list = api.get_member(176223, 1)
	#for img in illust_list:
	#	print img
	
	### Authentication required! call api.login first!
	#print ">>> get_bookmark(1418182, page=1)"
	#bookmark_list = api.get_bookmark(1418182, 1)
	#for img in bookmark_list:
	#	print img

	print ">>> ranking_log(2013-01-15, monthly, page=1)"
	rank_list = api.ranking_log('2013',1,'monthly','05','15')
	for img in rank_list:
		print img


if __name__ == '__main__':
	main()
