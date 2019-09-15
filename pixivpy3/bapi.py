# -*- coding:utf-8 -*-
"""
@author: Perol_Notsf
"""
import hashlib
import requests
from requests_toolbelt.adapters import host_header_ssl
from datetime import datetime
from .utils import PixivError
from .aapi import AppPixivAPI

class ByPassSniApi(AppPixivAPI):
    def __init__(self, **requests_kwargs):
        """initialize requests kwargs if need be"""
        super(AppPixivAPI, self).__init__(**requests_kwargs)
        self.hosts = "https://210.140.131.219"
        s = requests.Session()
        s.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
        self.requests = s
    def require_hostsip(self, hostname="app-api.pixiv.net"):
        """
        可选方法
        通过1.0.0.1请求真实的ip地址
        """
        url = "https://1.0.0.1/dns-query?ct=application/dns-json&name=%s&type=A&do=false&cd=false" % hostname
        response = requests.get(url)
        print(response.json())
        t = response.json()['Answer'][0]['data']
        self.hosts = "https://"+t

    def set_api_ipadress(self, ipaddress="https://210.140.131.219"):
        self.hosts = ipaddress

    def auth(self, username=None, password=None, refresh_token=None):
        """Login with password, or use the refresh_token to acquire a new bearer token"""
        # url = 'https://oauth.secure.pixiv.net/auth/token'
        url = '%s/auth/token' % self.hosts

        local_time = datetime.now().isoformat()
        headers = {
            'User-Agent': 'PixivAndroidApp/5.0.64 (Android 6.0)',
            'X-Client-Time': local_time,
            'X-Client-Hash': hashlib.md5((local_time + self.hash_secret).encode('utf-8')).hexdigest(),
            'host': 'oauth.secure.pixiv.net'
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

        r = self.requests_call('POST', url, headers=headers, data=data)
        if (r.status_code not in [200, 301, 302]):
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

    def no_auth_requests_call(self, method, url, headers={}, params=None, data=None, req_auth=True):
        headers['host'] = 'app-api.pixiv.net'
        if headers.get('User-Agent', None) == None and headers.get('user-agent', None) == None:
            # Set User-Agent if not provided
            headers['App-OS'] = 'ios'
            headers['App-OS-Version'] = '12.2'
            headers['App-Version'] = '7.6.2'
            headers['User-Agent'] = 'PixivIOSApp/7.6.2 (iOS 12.2; iPhone9,1)'
        if (not req_auth):
            return self.requests_call(method, url, headers, params, data)
        else:
            self.require_auth()
            headers['Authorization'] = 'Bearer %s' % self.access_token
            return self.requests_call(method, url, headers, params, data)
