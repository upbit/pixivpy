PixivPy
======
*Pixiv API for Python*

~~~~~ python
api = PixivAPI()

# WARNNING: login API no longer exists, it return 404 Not Found
#api.login("login", "username", "password", 0)

# get illust by id
illust = api.get_illust(36503804)
print illust
~~~~~
