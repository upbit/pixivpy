from .aapi import AppPixivAPI
from .async_.aapi import AppPixivAPI as AsyncAppPixivAPI
from .async_.papi import PixivAPI as AsyncPixivAPI
from .papi import PixivAPI
from .utils import PixivError


def asyncify():
    for name in dir(PixivAPI):
        if not name.startswith('_') or name == '__call__':
            setattr(PixivAPI, name, getattr(AsyncPixivAPI, name))

    for name in dir(AppPixivAPI):
        if not name.startswith('_') or name == '__call__':
            setattr(AppPixivAPI, name, getattr(AsyncAppPixivAPI, name))

    setattr(AppPixivAPI, 'dl', getattr(AsyncAppPixivAPI, 'dl'))


asyncify()

__all__ = ["PixivAPI", "AppPixivAPI", "PixivError"]
