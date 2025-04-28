"""Pixiv API library"""

from .aapi import AppPixivAPI
from .bapi import ByPassSniApi
from .utils import PixivError
from .webapi import WebPixivAPI  # Import the new class

__all__ = (
    "AppPixivAPI",
    "ByPassSniApi",
    "PixivError",
    "WebPixivAPI",
)  # Add the new class to __all__
