PixivPy
======
*Pixiv API for Python*

* [2014/10/07] new framework, **SAPI / Public-API** supported (requests needed)

First:

~~~~
pip install requests
~~~~

Example:

~~~~~ python
api = PixivAPI()

api.login("username", "password")

# get origin url
json_result = api.papi.get_works(45455208)
illust = json_result.response[0]
print "origin url: %s" % illust.image_urls['large']

### Authentication required! call api.login first!
print(">>> sapi.get_bookmark(1418182, page=1)")
bookmark_list = api.sapi.get_bookmark(1418182)
for img in bookmark_list:
	print(img)
~~~~~

Find Pixiv API in Objective-C? You might also like [PixivAPI_iOS](https://github.com/upbit/PixivAPI_iOS)
