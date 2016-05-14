"""
Pixiv API library
"""
__version__ = '3.1.1'

from .api import PixivAPI
from .utils import PixivError

__all__ = ("PixivAPI", "PixivError")
