"""
Pixiv API library
"""
__version__ = '3.4.0'

from .aapi import AppPixivAPI
from .papi import PixivAPI
from .utils import PixivError

__all__ = ("PixivAPI", "AppPixivAPI", "PixivError")
