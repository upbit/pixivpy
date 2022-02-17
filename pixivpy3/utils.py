# -*- coding:utf-8 -*-

import sys

if sys.version_info >= (3, 7):
    from typing import Any, Dict, Optional, Union

    from requests.structures import CaseInsensitiveDict

    ParamDict = Optional[Dict[str, Any]]
    ParsedJson = Any
    Response = Any


class PixivError(Exception):
    """Pixiv API exception"""

    def __init__(self, reason, header=None, body=None):
        # type: (str, Optional[Union[Dict[str, Any], CaseInsensitiveDict[Any]]], Optional[str]) -> None
        self.reason = str(reason)
        self.header = header
        self.body = body
        super(Exception, self).__init__(self, reason)

    def __str__(self):
        # type: () -> str
        return self.reason


class JsonDict(dict):  # type: ignore[type-arg]
    """general json object that allows attributes to be bound to and also behaves like a dict"""

    def __getattr__(self, attr):
        # type: (Any) -> Any
        return self.get(attr)

    def __setattr__(self, attr, value):
        # type: (Any, Any) -> None
        self[attr] = value
