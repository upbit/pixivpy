import pydantic
from pixivpy3 import AppPixivAPI

print(f"Current pydantic=={pydantic.__version__}")
_PYDANTIC_MAJOR_VERSION = int(pydantic.__version__.split(".")[0])
assert _PYDANTIC_MAJOR_VERSION >= 2

api = AppPixivAPI()
assert api is not None

print("SUCCESS!")
