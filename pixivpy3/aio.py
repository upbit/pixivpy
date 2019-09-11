import sys
from .utils import PixivError

if sys.version_info < (3, 6):
    raise PixivError('The version of python should >= 3.6 to use async.')

from .aapi import AppPixivAPI
from .papi import PixivAPI
import httpx
import asyncio
import logging


async def auth_req(self, url, headers, data):
    r = await self.req('POST', url, headers=headers, data=data)
    if r.status_code not in [200, 301, 302]:
        if data['grant_type'] == 'password':
            raise PixivError(
                '[ERROR] auth() failed! check username and password.\nHTTP %s: %s' % (r.status_code, r.text),
                header=r.headers, body=r.text)
        else:
            raise PixivError('[ERROR] auth() failed! check refresh_token.\nHTTP %s: %s' % (r.status_code, r.text),
                             header=r.headers, body=r.text)

    token = None
    try:
        # get access_token
        token = self.parse_json(r.text)
        self.access_token = token.response.access_token
        self.user_id = token.response.user.id
        self.refresh_token = token.response.refresh_token
    except:
        raise PixivError('Get access_token error! Response: %s' % token, header=r.headers, body=r.text)

    return token


async def async_requests_call(self, method, url, headers=None, params=None, data=None, stream=False):
    if headers is None:
        headers = {}
    w = await self.req(method, url, headers, params, data, stream)
    w.encoding = 'utf-8'
    print(w.url)
    return self.parse_result(w)


async def async_req(self, method, url, headers=None, params=None, data=None, stream=False):
    if headers is None:
        headers = {}
    client = httpx.AsyncClient()
    headers.update(self.additional_headers)
    try:
        if method == 'GET':
            return await client.get(url, params=params, headers=headers,
                                    stream=stream, **self.requests_kwargs)
        elif method == 'POST':
            return await client.post(url, params=params, data=data,
                                     headers=headers, stream=stream, **self.requests_kwargs)
        elif method == 'DELETE':
            return await client.delete(url, params=params, data=data,
                                       headers=headers, stream=stream, **self.requests_kwargs)
    except httpx.exceptions.ConnectTimeout:
        """Retry for timeout"""
        logging.warning('requests %s %s  timeout. retry 1 time...' % (method, url))
        await asyncio.sleep(1)
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


setattr(AppPixivAPI, 'auth_req', auth_req)
setattr(PixivAPI, 'auth_req', auth_req)
setattr(AppPixivAPI, 'requests_call', async_requests_call)
setattr(PixivAPI, 'requests_call', async_requests_call)
setattr(AppPixivAPI, 'req', async_req)
setattr(PixivAPI, 'req', async_req)

__all__ = ["PixivAPI", "AppPixivAPI", "PixivError"]
