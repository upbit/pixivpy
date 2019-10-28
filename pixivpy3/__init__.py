"""
Pixiv API library
"""
__version__ = '3.5.1'

from .papi import PixivAPI
from .aapi import AppPixivAPI
from .utils import PixivError

__all__ = ("PixivAPI", "AppPixivAPI", "PixivError")
