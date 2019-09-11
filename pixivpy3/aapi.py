# -*- coding:utf-8 -*-

import re
import sys

from .api import BasePixivAPI
from .utils import PixivError


# App-API (6.x - app-api.pixiv.net)
class AppPixivAPI(BasePixivAPI):

    def __init__(self, **requests_kwargs):
        """initialize requests kwargs if need be"""
        super(AppPixivAPI, self).__init__(**requests_kwargs)
        self.hosts = "https://app-api.pixiv.net"

    def set_api_proxy(self, proxy_hosts="http://app-api.pixivlite.com"):
        """Set proxy hosts: eg pixivlite.com"""
        self.hosts = proxy_hosts

    # Check auth and set BearerToken to headers
    def no_auth_requests_call(self, method, url, headers={}, params=None, data=None, req_auth=True):
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

    def format_bool(self, bool_value):
        if type(bool_value) == bool:
            return 'true' if bool_value else 'false'
        if bool_value in ['true', 'True']:
            return 'true'
        else:
            return 'false'

    # 返回翻页用参数
    def parse_qs(self, next_url):
        if not next_url: return None
        if sys.version_info >= (3, 0):
            from urllib.parse import urlparse, unquote
            safe_unquote = lambda s: unquote(s)
        else:
            from urlparse import urlparse, unquote
            safe_unquote = lambda s: unquote(s.encode('utf8')).decode('utf8')

        result_qs = {}
        query = urlparse(next_url).query
        for kv in query.split('&'):
            # split than unquote() to k,v strings
            k, v = map(safe_unquote, kv.split('='))

            # merge seed_illust_ids[] liked PHP params to array
            matched = re.match('(?P<key>[\w]*)\[(?P<idx>[\w]*)\]', k)
            if matched:
                mk = matched.group('key')
                marray = result_qs.get(mk, [])
                # keep the origin sequence, just ignore group('idx')
                result_qs[mk] = marray + [v]
            else:
                result_qs[k] = v

        return result_qs

    # 用户详情
    def user_detail(self, user_id, filter='for_ios', req_auth=True):
        url = '%s/v1/user/detail' % self.hosts
        params = {
            'user_id': user_id,
            'filter': filter,
        }
        return self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 用户作品列表
    # type: [illust, manga]
    def user_illusts(self, user_id, type='illust', filter='for_ios', offset=None, req_auth=True):
        url = '%s/v1/user/illusts' % self.hosts
        params = {
            'user_id': user_id,
            'filter': filter,
        }
        if type != None:
            params['type'] = type
        if (offset):
            params['offset'] = offset
        return self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 用户收藏作品列表
    # tag: 从 user_bookmark_tags_illust 获取的收藏标签
    def user_bookmarks_illust(self, user_id, restrict='public', filter='for_ios', max_bookmark_id=None, tag=None,
                              req_auth=True):
        url = '%s/v1/user/bookmarks/illust' % self.hosts
        params = {
            'user_id': user_id,
            'restrict': restrict,
            'filter': filter,
        }
        if (max_bookmark_id):
            params['max_bookmark_id'] = max_bookmark_id
        if (tag):
            params['tag'] = tag
        return self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 关注用户的新作
    # restrict: [public, private]
    def illust_follow(self, restrict='public', offset=None, req_auth=True):
        url = '%s/v2/illust/follow' % self.hosts
        params = {
            'restrict': restrict,
        }
        if (offset):
            params['offset'] = offset
        return self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 作品详情 (类似PAPI.works()，iOS中未使用)
    def illust_detail(self, illust_id, req_auth=True):
        url = '%s/v1/illust/detail' % self.hosts
        params = {
            'illust_id': illust_id,
        }
        return self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 作品评论
    def illust_comments(self, illust_id, offset=None, include_total_comments=None, req_auth=True):
        url = '%s/v1/illust/comments' % self.hosts
        params = {
            'illust_id': illust_id,
        }
        if (offset):
            params['offset'] = offset
        if (include_total_comments):
            params['include_total_comments'] = self.format_bool(include_total_comments)
        return self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 相关作品列表
    def illust_related(self, illust_id, filter='for_ios', seed_illust_ids=None, offset=None, req_auth=True):
        url = '%s/v2/illust/related' % self.hosts
        params = {
            'illust_id': illust_id,
            'filter': filter,
            'offset': offset,
        }
        if type(seed_illust_ids) == str:
            params['seed_illust_ids[]'] = [seed_illust_ids]
        if type(seed_illust_ids) == list:
            params['seed_illust_ids[]'] = seed_illust_ids
        return self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 插画推荐 (Home - Main)
    # content_type: [illust, manga]
    def illust_recommended(self, content_type='illust', include_ranking_label=True, filter='for_ios',
                           max_bookmark_id_for_recommend=None, min_bookmark_id_for_recent_illust=None,
                           offset=None, include_ranking_illusts=None, bookmark_illust_ids=None,
                           include_privacy_policy=None, req_auth=True):
        if (req_auth):
            url = '%s/v1/illust/recommended' % self.hosts
        else:
            url = '%s/v1/illust/recommended-nologin' % self.hosts
        params = {
            'content_type': content_type,
            'include_ranking_label': self.format_bool(include_ranking_label),
            'filter': filter,
        }
        if (max_bookmark_id_for_recommend):
            params['max_bookmark_id_for_recommend'] = max_bookmark_id_for_recommend
        if (min_bookmark_id_for_recent_illust):
            params['min_bookmark_id_for_recent_illust'] = min_bookmark_id_for_recent_illust
        if (offset):
            params['offset'] = offset
        if (include_ranking_illusts):
            params['include_ranking_illusts'] = self.format_bool(include_ranking_illusts)

        if (not req_auth):
            if (type(bookmark_illust_ids) == str):
                params['bookmark_illust_ids'] = bookmark_illust_ids
            if (type(bookmark_illust_ids) == list):
                params['bookmark_illust_ids'] = ",".join([str(iid) for iid in bookmark_illust_ids])

        if (include_privacy_policy):
            params['include_privacy_policy'] = include_privacy_policy

        return self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 作品排行
    # mode: [day, week, month, day_male, day_female, week_original, week_rookie, day_manga]
    # date: '2016-08-01'
    # mode (Past): [day, week, month, day_male, day_female, week_original, week_rookie,
    #               day_r18, day_male_r18, day_female_r18, week_r18, week_r18g]
    def illust_ranking(self, mode='day', filter='for_ios', date=None, offset=None, req_auth=True):
        url = '%s/v1/illust/ranking' % self.hosts
        params = {
            'mode': mode,
            'filter': filter,
        }
        if (date):
            params['date'] = date
        if (offset):
            params['offset'] = offset
        return self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 趋势标签 (Search - tags)
    def trending_tags_illust(self, filter='for_ios', req_auth=True):
        url = '%s/v1/trending-tags/illust' % self.hosts
        params = {
            'filter': filter,
        }
        return self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 搜索 (Search)
    # search_target - 搜索类型
    #   partial_match_for_tags  - 标签部分一致
    #   exact_match_for_tags    - 标签完全一致
    #   title_and_caption       - 标题说明文
    # sort: [date_desc, date_asc]
    # duration: [within_last_day, within_last_week, within_last_month]
    def search_illust(self, word, search_target='partial_match_for_tags', sort='date_desc', duration=None,
                      filter='for_ios', offset=None, req_auth=True):
        url = '%s/v1/search/illust' % self.hosts
        params = {
            'word': word,
            'search_target': search_target,
            'sort': sort,
            'filter': filter,
        }
        if (duration):
            params['duration'] = duration
        if (offset):
            params['offset'] = offset
        return self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 作品收藏详情
    def illust_bookmark_detail(self, illust_id, req_auth=True):
        url = '%s/v2/illust/bookmark/detail' % self.hosts
        params = {
            'illust_id': illust_id,
        }
        return self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 新增收藏
    def illust_bookmark_add(self, illust_id, restrict='public', tags=None, req_auth=True):
        url = '%s/v2/illust/bookmark/add' % self.hosts
        data = {
            'illust_id': illust_id,
            'restrict': restrict,
        }
        ## TODO: tags mast quote like 'tags=%E5%B0%BB%E7%A5%9E%E6%A7%98%20%E8%A3%B8%E8%B6%B3%20Fate%2FGO'
        # if (type(tags) == str):
        #     data['tags'] = tags
        # if (type(tags) == list):
        #     data['tags'] = " ".join([ str(tag) for tag in tags ])

        return self.no_auth_requests_call('POST', url, data=data, req_auth=req_auth)

    # 删除收藏
    def illust_bookmark_delete(self, illust_id, req_auth=True):
        url = '%s/v1/illust/bookmark/delete' % self.hosts
        data = {
            'illust_id': illust_id,
        }
        return self.no_auth_requests_call('POST', url, data=data, req_auth=req_auth)

    # 用户收藏标签列表
    def user_bookmark_tags_illust(self, restrict='public', offset=None, req_auth=True):
        url = '%s/v1/user/bookmark-tags/illust' % self.hosts
        params = {
            'restrict': restrict,
        }
        if (offset):
            params['offset'] = offset
        return self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # Following用户列表
    def user_following(self, user_id, restrict='public', offset=None, req_auth=True):
        url = '%s/v1/user/following' % self.hosts
        params = {
            'user_id': user_id,
            'restrict': restrict,
        }
        if (offset):
            params['offset'] = offset
        return self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # Followers用户列表
    def user_follower(self, user_id, filter='for_ios', offset=None, req_auth=True):
        url = '%s/v1/user/follower' % self.hosts
        params = {
            'user_id': user_id,
            'filter': filter,
        }
        if (offset):
            params['offset'] = offset

        r = self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 好P友
    def user_mypixiv(self, user_id, offset=None, req_auth=True):
        url = '%s/v1/user/mypixiv' % self.hosts
        params = {
            'user_id': user_id,
        }
        if (offset):
            params['offset'] = offset
        return self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 黑名单用户
    def user_list(self, user_id, filter='for_ios', offset=None, req_auth=True):
        url = '%s/v2/user/list' % self.hosts
        params = {
            'user_id': user_id,
            'filter': filter,
        }
        if (offset):
            params['offset'] = offset

        return self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 获取ugoira信息
    def ugoira_metadata(self, illust_id, req_auth=True):
        url = '%s/v1/ugoira/metadata' % self.hosts
        params = {
            'illust_id': illust_id,
        }

        return self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 特辑详情 (无需登录，调用Web API)
    def showcase_article(self, showcase_id):
        url = 'https://www.pixiv.net/ajax/showcase/article'
        # Web API，伪造Chrome的User-Agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/63.0.3239.132 Safari/537.36',
            'Referer': 'https://www.pixiv.net',
        }
        params = {
            'article_id': showcase_id,
        }

        return self.no_auth_requests_call('GET', url, headers=headers, params=params, req_auth=False)
