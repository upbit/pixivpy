# -*- coding:utf-8 -*-

from .api import BasePixivAPI


# Public-API

class PixivAPI(BasePixivAPI):
    def __init__(self, **requests_kwargs):
        """
        initialize requests kwargs if need be
        """
        self.prefix = 'https://public-api.secure.pixiv.net/v1.1/'
        self.api = 'https://public-api.secure.pixiv.net/v1/'
        super().__init__(**requests_kwargs)

    async def auth_requests_call(self, method, url, params=None, data=None, headers=None):
        self.require_auth()
        headers = dict() if headers is None else headers
        headers.update({
            'Referer': 'http://spapi.pixiv.net/',
            'User-Agent': 'PixivIOSApp/5.8.7',
            'Authorization': 'Bearer {}'.format(self.access_token)
        })
        return await self.requests_call(method, url, headers=headers, params=params, data=data)

    async def bad_words(self):
        url = self.prefix + 'bad_words.json'
        r = await self.auth_requests_call('GET', url)
        return self.parse_json(r)

    async def works(self, illust_id=121827112, include_sanity_level=False):
        url = '{}/works/{}.json'.format(self.api, illust_id)
        params = {
            'image_sizes': 'px_128x128,small,medium,large,px_480mw',
            'include_stats': 'true',
            'include_sanity_level': str(include_sanity_level).lower()
        }
        r = await self.auth_requests_call('GET', url, params=params)
        return self.parse_json(r)

    async def users(self, author_id):
        url = '{}/users/{}.json'.format(self.api, author_id)
        params = {
            'profile_image_sizes': 'px_170x170,px_50x50',
            'image_sizes': 'px_128x128,small,medium,large,px_480mw',
            'include_stats': 1,
            'include_profile': 1,
            'include_workspace': 1,
            'include_contacts': 1,
        }
        r = await self.auth_requests_call('GET', url, params=params)
        return self.parse_json(r)

    async def me_feeds(self, show_r18=1, max_id=None):
        url = 'https://public-api.secure.pixiv.net/v1/me/feeds.json'
        params = {
            'relation': 'all',
            'type': 'touch_nottext',
            'show_r18': show_r18,
        }
        if max_id:
            params['max_id'] = max_id
        r = await self.auth_requests_call('GET', url, params=params)
        return self.parse_json(r)

    async def me_favorite_works(self, page=1, per_page=50, publicity='public', image_sizes=None):
        if image_sizes is None:
            image_sizes = ['px_128x128', 'px_480mw', 'large']
        url = 'https://public-api.secure.pixiv.net/v1/me/favorite_works.json'
        params = {
            'page': page,
            'per_page': per_page,
            'publicity': publicity,
            'image_sizes': ','.join(image_sizes),
        }
        r = await self.auth_requests_call('GET', url, params=params)
        return self.parse_json(r)

    async def me_favorite_works_add(self, work_id, publicity='public'):
        url = 'https://public-api.secure.pixiv.net/v1/me/favorite_works.json'
        params = {
            'work_id': work_id,
            'publicity': publicity,
        }
        r = await self.auth_requests_call('POST', url, params=params)
        return self.parse_json(r)

    async def me_favorite_works_delete(self, ids, publicity='public'):
        url = 'https://public-api.secure.pixiv.net/v1/me/favorite_works.json'
        if isinstance(ids, list):
            params = {
                'ids': ",".join(map(str, ids)),
                'publicity': publicity
            }
        else:
            params = {
                'ids': ids,
                'publicity': publicity
            }
        r = await self.auth_requests_call('DELETE', url, params=params)
        return self.parse_json(r)

    async def me_following_works(self, page=1, per_page=30,
                                 image_sizes=None,
                                 include_stats=True, include_sanity_level=True):
        if image_sizes is None:
            image_sizes = ['px_128x128', 'px_480mw', 'large']
        url = 'https://public-api.secure.pixiv.net/v1/me/following/works.json'
        params = {
            'page': page,
            'per_page': per_page,
            'image_sizes': ','.join(image_sizes),
            'include_stats': include_stats,
            'include_sanity_level': include_sanity_level,
        }
        r = await self.auth_requests_call('GET', url, params=params)
        return self.parse_json(r)

    async def me_following(self, page=1, per_page=30, publicity='public'):
        url = 'https://public-api.secure.pixiv.net/v1/me/following.json'
        params = {
            'page': page,
            'per_page': per_page,
            'publicity': publicity,
        }
        r = await self.auth_requests_call('GET', url, params=params)
        return self.parse_json(r)

    async def me_favorite_users_follow(self, user_id, publicity='public'):
        url = 'https://public-api.secure.pixiv.net/v1/me/favorite-users.json'
        params = {
            'target_user_id': user_id,
            'publicity': publicity
        }
        r = await self.auth_requests_call('POST', url, params=params)
        return self.parse_json(r)

    async def me_favorite_users_unfollow(self, user_ids, publicity='public'):
        url = 'https://public-api.secure.pixiv.net/v1/me/favorite-users.json'
        if type(user_ids) == list:
            params = {'delete_ids': ",".join(map(str, user_ids)), 'publicity': publicity}
        else:
            params = {'delete_ids': user_ids, 'publicity': publicity}
        r = await self.auth_requests_call('DELETE', url, params=params)
        return self.parse_json(r)

    async def users_works(self, author_id, page=1, per_page=30,
                          image_sizes=None,
                          include_stats=True, include_sanity_level=True):
        if image_sizes is None:
            image_sizes = ['px_128x128', 'px_480mw', 'large']
        url = 'https://public-api.secure.pixiv.net/v1/users/%d/works.json' % author_id
        params = {
            'page': page,
            'per_page': per_page,
            'include_stats': include_stats,
            'include_sanity_level': include_sanity_level,
            'image_sizes': ','.join(image_sizes),
        }
        r = await self.auth_requests_call('GET', url, params=params)
        return self.parse_json(r)

    async def users_favorite_works(self, author_id, page=1, per_page=30,
                                   image_sizes=None,
                                   include_sanity_level=True):
        if image_sizes is None:
            image_sizes = ['px_128x128', 'px_480mw', 'large']
        url = 'https://public-api.secure.pixiv.net/v1/users/%d/favorite_works.json' % author_id
        params = {
            'page': page,
            'per_page': per_page,
            'include_sanity_level': include_sanity_level,
            'image_sizes': ','.join(image_sizes),
        }
        r = await self.auth_requests_call('GET', url, params=params)
        return self.parse_json(r)

    async def users_feeds(self, author_id, show_r18=1, max_id=None):
        url = 'https://public-api.secure.pixiv.net/v1/users/%d/feeds.json' % author_id
        params = {
            'relation': 'all',
            'type': 'touch_nottext',
            'show_r18': show_r18,
        }
        if max_id:
            params['max_id'] = max_id
        r = await self.auth_requests_call('GET', url, params=params)
        return self.parse_json(r)

    async def users_following(self, author_id, page=1, per_page=30):
        url = 'https://public-api.secure.pixiv.net/v1/users/%d/following.json' % author_id
        params = {
            'page': page,
            'per_page': per_page,
        }
        r = await self.auth_requests_call('GET', url, params=params)
        return self.parse_json(r)

    async def ranking(self, ranking_type='all', mode='daily', page=1, per_page=50, date=None,
                      image_sizes=None,
                      profile_image_sizes=None,
                      include_stats=True, include_sanity_level=True):
        if profile_image_sizes is None:
            profile_image_sizes = ['px_170x170', 'px_50x50']
        if image_sizes is None:
            image_sizes = ['px_128x128', 'px_480mw', 'large']
        url = 'https://public-api.secure.pixiv.net/v1/ranking/%s.json' % ranking_type
        params = {
            'mode': mode,
            'page': page,
            'per_page': per_page,
            'include_stats': include_stats,
            'include_sanity_level': include_sanity_level,
            'image_sizes': ','.join(image_sizes),
            'profile_image_sizes': ','.join(profile_image_sizes),
        }
        if date:
            params['date'] = date
        r = await self.auth_requests_call('GET', url, params=params)
        return self.parse_json(r)

    # 作品搜索
    async def search_works(self, query, page=1, per_page=30, mode='text',
                           period='all', order='desc', sort='date',
                           types=None,
                           image_sizes=None,
                           include_stats=True, include_sanity_level=True):
        if image_sizes is None:
            image_sizes = ['px_128x128', 'px_480mw', 'large']
        if types is None:
            types = ['illustration', 'manga', 'ugoira']
        url = 'https://public-api.secure.pixiv.net/v1/search/works.json'
        params = {
            'q': query,
            'page': page,
            'per_page': per_page,
            'period': period,
            'order': order,
            'sort': sort,
            'mode': mode,
            'types': ','.join(types),
            'include_stats': include_stats,
            'include_sanity_level': include_sanity_level,
            'image_sizes': ','.join(image_sizes),
        }
        r = await self.auth_requests_call('GET', url, params=params)
        return self.parse_json(r)

    # 最新作品 (New -> Everyone)
    async def latest_works(self, page=1, per_page=30,
                           image_sizes=None,
                           profile_image_sizes=None,
                           include_stats=True, include_sanity_level=True):
        if profile_image_sizes is None:
            profile_image_sizes = ['px_170x170', 'px_50x50']
        if image_sizes is None:
            image_sizes = ['px_128x128', 'px_480mw', 'large']
        url = 'https://public-api.secure.pixiv.net/v1/works.json'
        params = {
            'page': page,
            'per_page': per_page,
            'include_stats': include_stats,
            'include_sanity_level': include_sanity_level,
            'image_sizes': ','.join(image_sizes),
            'profile_image_sizes': ','.join(profile_image_sizes),
        }
        r = await self.auth_requests_call('GET', url, params=params)
        return self.parse_json(r)

    def ranking_all(self, mode='daily', page=1, per_page=50, date=None,
                    image_sizes=None,
                    profile_image_sizes=None,
                    include_stats=True,
                    include_sanity_level=True):
        if profile_image_sizes is None:
            profile_image_sizes = ['px_170x170', 'px_50x50']
        if image_sizes is None:
            image_sizes = ['px_128x128', 'px_480mw', 'large']
        return self.ranking(ranking_type='all', mode=mode, page=page, per_page=per_page, date=date,
                            image_sizes=image_sizes, profile_image_sizes=profile_image_sizes,
                            include_stats=include_stats, include_sanity_level=include_sanity_level)

    def parse_result(self, req):
        pass
