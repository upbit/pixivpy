# -*- coding:utf-8 -*-
import hashlib
import json
import os
from datetime import datetime

import aiohttp

from ..utils import PixivError, JsonDict


class BasePixivAPI:
    client_id = 'MOBrBDS8blbauoSck0ZfDbtuzpyT'
    client_secret = 'lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj'
    hash_secret = '28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c'

    access_token = None
    user_id = 0
    refresh_token = None

    def __init__(self, **requests_kwargs):
        self.requests = None
        self.requests_kwargs = requests_kwargs
        self.additional_headers = {}

    def set_auth(self, access_token, refresh_token=None):
        self.access_token = access_token
        self.refresh_token = refresh_token

    def require_auth(self):
        if self.access_token is None:
            raise PixivError('No access_token Found!')

    def login(self, username, password):
        return self.auth(username=username, password=password)

    def set_additional_headers(self, headers):
        self.additional_headers = headers

    def set_client(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def set_accept_language(self, language):
        self.additional_headers['Accept-Language'] = language

    async def dl(self, url, headers=None):
        if headers is None:
            headers = {}
        headers.update(self.additional_headers)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.read()

    async def requests_call(self, method, url, headers=None, data=None, params=None):
        if data is None:
            data = dict()
        if params is None:
            params = dict()
        if headers is None:
            headers = dict()
        headers.update(self.additional_headers)

        async def fetch(_session, _url, _headers, _params):
            async with _session.get(_url, headers=_headers, params=_params) as response:
                return await response.json()

        async def post(_session, _url, _data, _headers, _params):
            async with _session.post(_url, data=_data, headers=_headers, params=_params) as response:
                return await response.json()

        async def delete(_session, _url, _headers, _params):
            async with _session.delete(_url, headers=_headers, params=_params) as response:
                return await response.json()

        if method == 'GET':
            async with aiohttp.ClientSession() as session:
                return await fetch(session, url, headers, params)
        elif method == 'POST':
            async with aiohttp.ClientSession() as session:
                return await post(session, url, data, headers, params)
        elif method == 'DELETE':
            async with aiohttp.ClientSession() as session:
                return await delete(session, url, headers, params)
        else:
            raise PixivError('Unknow method: %s' % method)

    async def auth(self, username=None, password=None, refresh_token=None):
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

        if username and password:
            data['grant_type'] = 'password'
            data['username'] = username
            data['password'] = password
        elif refresh_token or self.refresh_token:
            data['grant_type'] = 'refresh_token'
            data['refresh_token'] = refresh_token or self.refresh_token
        else:
            raise PixivError('[ERROR] auth() but no password or refresh_token is set.')

        token = await self.requests_call('POST', url, headers=headers, data=data)
        token = self.parse_json(token)
        self.access_token = token.response.access_token
        self.user_id = token.response.user.id
        self.refresh_token = token.response.refresh_token
        return token

    async def download(self, url, prefix='', path=os.path.curdir,
                       name=None, replace=False, referer='https://app-api.pixiv.net/'):
        if not name:
            name = prefix + os.path.basename(url)
        else:
            name = prefix + name

        img_path = os.path.join(path, name)

        if not os.path.exists(img_path) or replace:
            e = await self.dl(url, headers={'Referer': referer})
            with open(img_path, 'wb') as out_file:
                out_file.write(e)
            del e

    def parse_json(self, _):
        def _obj_hook(pairs):
            o = JsonDict()
            for k, v in pairs.items():
                o[str(k)] = v
            return o

        return json.loads(json.dumps(_), object_hook=_obj_hook)
