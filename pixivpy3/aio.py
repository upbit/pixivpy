import sys
from .utils import PixivError

if sys.version_info < (3, 6):
    raise PixivError('The version of python should >= 3.6 to use async.')

from .aapi import AppPixivAPI
from .papi import PixivAPI
import httpx


async def async_requests_call(self, method, url, headers={}, params=None, data=None, stream=False):
    w = await self.req(method, url, headers, params, data, stream)
    w.encoding = 'utf-8'
    return self.parse_result(w)


async def async_req(self, method, url, headers={}, params=None, data=None, stream=False):
    client = httpx.AsyncClient()
    headers.update(self.additional_headers)
    try:
        if method == 'GET':
            return await client.get(url, params=params, headers=headers, stream=stream,
                              **self.requests_kwargs)
        elif method == 'POST':
            return await client.post(url, params=params, data=data, headers=headers, stream=stream,
                               **self.requests_kwargs)
        elif method == 'DELETE':
            return await client.delete(url, params=params, data=data, headers=headers, stream=stream,
                                 **self.requests_kwargs)
    except Exception as e:
        raise PixivError('requests %s %s error: %s' % (method, url, e))

    raise PixivError('Unknow method: %s' % method)

setattr(AppPixivAPI, 'requests_call', async_requests_call)
setattr(PixivAPI, 'requests_call', async_requests_call)
setattr(AppPixivAPI, 'req', async_req)
setattr(PixivAPI, 'req', async_req)

__all__ = ["PixivAPI", "AppPixivAPI", "PixivError"]
