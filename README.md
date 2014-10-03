PixivPy
======
*Pixiv API for Python*

~~~~~ python
api = PixivAPI()

# WARNNING: login() deprecated, use login2() instand
#api.login2("username", "password")

# get illust by id
illust = api.get_illust(36503804)
print(illust)
~~~~~

Find Pixiv API in Objective-C? You might also like [PixivAPI_iOS](https://github.com/upbit/PixivAPI_iOS)
