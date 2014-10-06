#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

from pixivpy2 import *

_USERNAME = "username"
_PASSWORD = "password"

def main():
	api = PixivAPI()

	### change _USERNAME,_PASSWORD first!
	api.login(_USERNAME, _PASSWORD)

	json_result = api.papi.get_works(45455208)
	print json_result
	
	illust = json_result.response[0]
	print illust
	print "  large: %s" % illust.image_urls['large']
	print " medium: %s" % illust.image_urls['medium']

	### Authentication required! call api.login first!
	#print(">>> sapi.get_bookmark(1418182, page=1)")
	#bookmark_list = api.sapi.get_bookmark(1418182)
	#for img in bookmark_list:
	#	print(img)

if __name__ == '__main__':
	main()
