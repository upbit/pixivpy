"""
Pixiv API library
"""
__version__ = '3.4.0'

from .papi import PixivAPI
from .aapi import AppPixivAPI
from .utils import PixivError

__all__ = ("PixivAPI", "AppPixivAPI", "PixivError")
