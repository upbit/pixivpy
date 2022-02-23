# -*- coding:utf-8 -*-

from typing import Any, Dict, Optional, Union

from requests.structures import CaseInsensitiveDict

ParamDict = Optional[Dict[str, Any]]
ParsedJson = Any
Response = Any


class PixivError(Exception):
    """Pixiv API exception"""

    def __init__(
        self,
        reason: str,
        header: Optional[Union[Dict[str, Any], CaseInsensitiveDict[Any]]] = None,
        body: Optional[str] = None,
    ) -> None:
        self.reason = str(reason)
        self.header = header
        self.body = body
        super(Exception, self).__init__(self, reason)

    def __str__(self) -> str:
        return self.reason


class JsonDict(dict):  # type: ignore[type-arg]
    """general json object that allows attributes to be bound to and also behaves like a dict"""

    def __getattr__(self, attr: Any) -> Any:
        return self.get(attr)

    def __setattr__(self, attr: Any, value: Any) -> None:
        self[attr] = value
