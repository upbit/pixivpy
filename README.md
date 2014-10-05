PixivPy
======
*Pixiv API for Python*

<span style="color:#F00;">**Since @Pixiv switch to Public-API(V1), SAPI versions will stop updating.**</span>

Please check the [master](https://github.com/upbit/pixivpy/tree/master) branch for more information.

~~~~~ python
api = PixivAPI()

# WARNNING: login() deprecated, use login2() instand
#api.login2("username", "password")

# get illust by id
illust = api.get_illust(36503804)
print(illust)
~~~~~

Find Pixiv API in Objective-C? You might also like [PixivAPI_iOS](https://github.com/upbit/PixivAPI_iOS)
