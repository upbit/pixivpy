import sys
from .utils import PixivError

if sys.version_info < (3, 6):
    raise PixivError('The version of python should >= 3.6 to use async.')

from datetime import datetime
from .aapi import AppPixivAPI
from .papi import PixivAPI
import httpx
import hashlib


async def async_auth(self, username=None, password=None, refresh_token=None):
    """Login with password, or use the refresh_token to acquire a new bearer token"""

    url = 'https://oauth.secure.pixiv.net/auth/token'
    local_time = datetime.now().isoformat()
    headers = {
        'User-Agent': 'PixivAndroidApp/5.0.64 (Android 6.0)',
        'X-Client-Time': local_time,
        'X-Client-Hash': hashlib.md5((local_time + self.hash_secret).encode('utf-8')).hexdigest(),
    }
    data = {
        'get_secure_url': 1,
        'client_id': self.client_id,
        'client_secret': self.client_secret,
    }

    if (username is not None) and (password is not None):
        data['grant_type'] = 'password'
        data['username'] = username
        data['password'] = password
    elif (refresh_token is not None) or (self.refresh_token is not None):
        data['grant_type'] = 'refresh_token'
        data['refresh_token'] = refresh_token or self.refresh_token
    else:
        raise PixivError('[ERROR] auth() but no password or refresh_token is set.')

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
        raise PixivError('Get access_token error! Response: %s' % (token), header=r.headers, body=r.text)

    # return auth/token response
    return token


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


setattr(AppPixivAPI, 'auth', async_auth)
setattr(PixivAPI, 'auth', async_auth)
setattr(AppPixivAPI, 'requests_call', async_requests_call)
setattr(PixivAPI, 'requests_call', async_requests_call)
setattr(AppPixivAPI, 'req', async_req)
setattr(PixivAPI, 'req', async_req)

__all__ = ["PixivAPI", "AppPixivAPI", "PixivError"]
