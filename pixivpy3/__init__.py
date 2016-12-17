"""
Pixiv API library
"""
__version__ = '3.2.2'

from .papi import PixivAPI
from .aapi import AppPixivAPI
from .utils import PixivError

__all__ = ("PixivAPI", "AppPixivAPI", "PixivError")
