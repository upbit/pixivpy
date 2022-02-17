# -*- coding:utf-8 -*-

import re
import sys

from .api import BasePixivAPI  # nopep8
from .utils import PixivError  # nopep8

if sys.version_info >= (3, 0):
    import urllib.parse as up
else:
    import urlparse as up

if sys.version_info >= (3, 7):
    from typing import Any, Dict, List, Optional, Union

    from .utils import ParsedJson, ParamDict, Response  # nopep8

from requests.structures import CaseInsensitiveDict


# App-API (6.x - app-api.pixiv.net)
# noinspection PyShadowingBuiltins
class AppPixivAPI(BasePixivAPI):
    def __init__(self, **requests_kwargs):
        # type: (Any) -> None
        """initialize requests kwargs if need be"""
        super(AppPixivAPI, self).__init__(**requests_kwargs)
        self.hosts = "https://app-api.pixiv.net"

    # noinspection HttpUrlsUsage
    def set_api_proxy(self, proxy_hosts="http://app-api.pixivlite.com"):
        # type: (str) -> None
        """Set proxy hosts: eg pixivlite.com"""
        self.hosts = proxy_hosts

    # Check auth and set BearerToken to headers
    def no_auth_requests_call(
        self, method, url, headers=None, params=None, data=None, req_auth=True
    ):
        # type: (str, str, ParamDict, ParamDict, ParamDict, bool) -> Response
        headers_ = CaseInsensitiveDict(headers or {})
        if self.hosts != "https://app-api.pixiv.net":
            headers_["host"] = "app-api.pixiv.net"
        if "user-agent" not in headers_:
            # Set User-Agent if not provided
            headers_["app-os"] = "ios"
            headers_["app-os-version"] = "14.6"
            headers_["user-agent"] = "PixivIOSApp/7.13.3 (iOS 14.6; iPhone13,2)"

        if not req_auth:
            return self.requests_call(method, url, headers_, params, data)
        else:
            self.require_auth()
            headers_["Authorization"] = "Bearer %s" % self.access_token
            return self.requests_call(method, url, headers_, params, data)

    def parse_result(self, res):
        # type: (Response) -> ParsedJson
        try:
            return self.parse_json(res.text)
        except Exception as e:
            raise PixivError(
                "parse_json() error: %s" % e, header=res.headers, body=res.text
            )

    @classmethod
    def format_bool(cls, bool_value):
        # type: (Union[bool, str]) -> str
        if isinstance(bool_value, bool):
            return "true" if bool_value else "false"
        if bool_value in {"true", "True"}:
            return "true"
        else:
            return "false"

    # 返回翻页用参数
    @classmethod
    def parse_qs(cls, next_url):
        # type: (str) -> Optional[Dict[str, Union[str, List[str]]]]
        if not next_url:
            return None

        result_qs = {}  # type: Dict[str, Union[str, List[str]]]
        query = up.urlparse(next_url).query

        if sys.version_info >= (3, 0):
            for key, value in up.parse_qs(query).items():
                # merge seed_illust_ids[] liked PHP params to array
                if "[" in key and key.endswith("]"):
                    # keep the origin sequence, just ignore array length
                    result_qs[key.split("[")[0]] = value
                else:
                    result_qs[key] = value[-1]

        else:
            # Python2 unquote may return utf8 instead of unicode
            def safe_unquote(s):
                return up.unquote(s.encode("utf8")).decode("utf8")

            for kv in query.split("&"):
                # split than unquote() to k,v strings
                k, v = map(safe_unquote, kv.split("="))

                # merge seed_illust_ids[] liked PHP params to array
                matched = re.match("(?P<key>[\w]*)\[(?P<idx>[\w]*)\]", k)
                if matched:
                    mk = matched.group("key")
                    marray = result_qs.get(mk, [])
                    # keep the origin sequence, just ignore group('idx')
                    result_qs[mk] = marray + [v]
                else:
                    result_qs[k] = v

        return result_qs

    # 用户详情
    def user_detail(self, user_id, filter="for_ios", req_auth=True):
        # type: (Union[int, str], str, bool) -> ParsedJson
        url = "%s/v1/user/detail" % self.hosts
        params = {
            "user_id": user_id,
            "filter": filter,
        }
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 用户作品列表
    ## type: [illust, manga]
    def user_illusts(
        self, user_id, type="illust", filter="for_ios", offset=None, req_auth=True
    ):
        # type: (Union[int, str], str, str, Optional[Union[int, str]], bool) -> ParsedJson
        url = "%s/v1/user/illusts" % self.hosts
        params = {
            "user_id": user_id,
            "filter": filter,
        }
        if type is not None:
            params["type"] = type
        if offset:
            params["offset"] = offset
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 用户收藏作品列表
    # tag: 从 user_bookmark_tags_illust 获取的收藏标签
    def user_bookmarks_illust(
        self,
        user_id,
        restrict="public",
        filter="for_ios",
        max_bookmark_id=None,
        tag=None,
        req_auth=True,
    ):
        # type: (Union[int, str], str, str, Optional[Union[int, str]], Optional[str], bool) -> ParsedJson
        url = "%s/v1/user/bookmarks/illust" % self.hosts
        params = {
            "user_id": user_id,
            "restrict": restrict,
            "filter": filter,
        }
        if max_bookmark_id:
            params["max_bookmark_id"] = max_bookmark_id
        if tag:
            params["tag"] = tag
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    def user_related(self, seed_user_id, filter="for_ios", offset=None, req_auth=True):
        # type: (Union[int, str], str, Optional[Union[int, str]], bool) -> ParsedJson
        url = "%s/v1/user/related" % self.hosts
        params = {
            "filter": filter,
            # Pixiv warns to put seed_user_id at the end -> put offset here
            "offset": offset if offset else 0,
            "seed_user_id": seed_user_id,
        }
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 关注用户的新作
    # restrict: [public, private]
    def illust_follow(self, restrict="public", offset=None, req_auth=True):
        # type: (str, Optional[Union[int, str]], bool) ->ParsedJson
        url = "%s/v2/illust/follow" % self.hosts
        params = {
            "restrict": restrict,
        }  # type: Dict[str, str|int]
        if offset:
            params["offset"] = offset
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 作品详情 (类似PAPI.works()，iOS中未使用)
    def illust_detail(self, illust_id, req_auth=True):
        # type: (Union[int, str], bool) -> ParsedJson
        url = "%s/v1/illust/detail" % self.hosts
        params = {
            "illust_id": illust_id,
        }
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 作品评论
    def illust_comments(
        self, illust_id, offset=None, include_total_comments=None, req_auth=True
    ):
        # type: (Union[int, str], Optional[Union[int, str]], Optional[Union[str, bool]], bool) -> ParsedJson
        url = "%s/v1/illust/comments" % self.hosts
        params = {
            "illust_id": illust_id,
        }
        if offset:
            params["offset"] = offset
        if include_total_comments:
            params["include_total_comments"] = self.format_bool(include_total_comments)
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 相关作品列表
    def illust_related(
        self,
        illust_id,
        filter="for_ios",
        seed_illust_ids=None,
        offset=None,
        viewed=None,
        req_auth=True,
    ):
        # type: (Union[int, str], str, Optional[Union[int, str]], Optional[Union[int, str]], Optional[str], bool) -> ParsedJson
        url = "%s/v2/illust/related" % self.hosts
        params = {
            "illust_id": illust_id,
            "filter": filter,
            "offset": offset,
        }  # type: Dict[str, Any]
        if isinstance(seed_illust_ids, str):
            params["seed_illust_ids[]"] = [seed_illust_ids]
        elif isinstance(seed_illust_ids, list):
            params["seed_illust_ids[]"] = seed_illust_ids
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 插画推荐 (Home - Main)
    # content_type: [illust, manga]
    def illust_recommended(
        self,
        content_type="illust",
        include_ranking_label=True,
        filter="for_ios",
        max_bookmark_id_for_recommend=None,
        min_bookmark_id_for_recent_illust=None,
        offset=None,
        include_ranking_illusts=None,
        bookmark_illust_ids=None,
        include_privacy_policy=None,
        viewed=None,
        req_auth=True,
    ):
        # type: (str, bool, str, Optional[Union[int, str]], Optional[Union[int, str]], Optional[Union[int, str]], Optional[Union[str, bool]], Optional[Union[str, List[Union[int, str]]]], Optional[Union[str, bool]], Optional[str], bool) -> ParsedJson
        if req_auth:
            url = "%s/v1/illust/recommended" % self.hosts
        else:
            url = "%s/v1/illust/recommended-nologin" % self.hosts
        params = {
            "content_type": content_type,
            "include_ranking_label": self.format_bool(include_ranking_label),
            "filter": filter,
        }  # type: Dict[str, Any]
        if max_bookmark_id_for_recommend:
            params["max_bookmark_id_for_recommend"] = max_bookmark_id_for_recommend
        if min_bookmark_id_for_recent_illust:
            params[
                "min_bookmark_id_for_recent_illust"
            ] = min_bookmark_id_for_recent_illust
        if offset:
            params["offset"] = offset
        if include_ranking_illusts:
            params["include_ranking_illusts"] = self.format_bool(
                include_ranking_illusts
            )

        if not req_auth:
            if isinstance(bookmark_illust_ids, str):
                params["bookmark_illust_ids"] = bookmark_illust_ids
            elif isinstance(bookmark_illust_ids, list):
                params["bookmark_illust_ids"] = ",".join(
                    str(iid) for iid in bookmark_illust_ids
                )

        if include_privacy_policy:
            params["include_privacy_policy"] = include_privacy_policy

        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 作品排行
    # mode: [day, week, month, day_male, day_female, week_original, week_rookie, day_manga]
    # date: '2016-08-01'
    # mode (Past): [day, week, month, day_male, day_female, week_original, week_rookie,
    #               day_r18, day_male_r18, day_female_r18, week_r18, week_r18g]
    def illust_ranking(
        self, mode="day", filter="for_ios", date=None, offset=None, req_auth=True
    ):
        # type: (str, str, Optional[str], Optional[Union[int, str]], bool) -> ParsedJson
        url = "%s/v1/illust/ranking" % self.hosts
        params = {
            "mode": mode,
            "filter": filter,
        }  # type: Dict[str, Any]
        if date:
            params["date"] = date
        if offset:
            params["offset"] = offset
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 趋势标签 (Search - tags)
    def trending_tags_illust(self, filter="for_ios", req_auth=True):
        # type: (str, bool) -> ParsedJson
        url = "%s/v1/trending-tags/illust" % self.hosts
        params = {
            "filter": filter,
        }
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 搜索 (Search)
    # search_target - 搜索类型
    #   partial_match_for_tags  - 标签部分一致
    #   exact_match_for_tags    - 标签完全一致
    #   title_and_caption       - 标题说明文
    # sort: [date_desc, date_asc, popular_desc] - popular_desc为会员的热门排序
    # duration: [within_last_day, within_last_week, within_last_month]
    # start_date, end_date: '2020-07-01'
    def search_illust(
        self,
        word,
        search_target="partial_match_for_tags",
        sort="date_desc",
        duration=None,
        start_date=None,
        end_date=None,
        filter="for_ios",
        offset=None,
        req_auth=True,
    ):
        # type: (str, str, str, Optional[str], Optional[str], Optional[str], Optional[str], Optional[Union[int, str]], bool) -> ParsedJson
        url = "%s/v1/search/illust" % self.hosts
        params = {
            "word": word,
            "search_target": search_target,
            "sort": sort,
            "filter": filter,
        }  # type: Dict[str, Any]
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if duration:
            params["duration"] = duration
        if offset:
            params["offset"] = offset
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 搜索小说 (Search Novel)
    # search_target - 搜索类型
    #   partial_match_for_tags  - 标签部分一致
    #   exact_match_for_tags    - 标签完全一致
    #   text                    - 正文
    #   keyword                 - 关键词
    # sort: [date_desc, date_asc]
    # start_date/end_date: 2020-06-01
    def search_novel(
        self,
        word,
        search_target="partial_match_for_tags",
        sort="date_desc",
        merge_plain_keyword_results="true",
        include_translated_tag_results="true",
        start_date=None,
        end_date=None,
        filter=None,
        offset=None,
        req_auth=True,
    ):
        # type: (str, str, str, str, str, Optional[str], Optional[str], Optional[str], Optional[Union[int, str]], bool) -> ParsedJson
        url = "%s/v1/search/novel" % self.hosts
        params = {
            "word": word,
            "search_target": search_target,
            "merge_plain_keyword_results": merge_plain_keyword_results,
            "include_translated_tag_results": include_translated_tag_results,
            "sort": sort,
            "filter": filter,
        }  # type: Dict[str, Any]
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if offset:
            params["offset"] = offset
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    def search_user(
        self,
        word,
        sort="date_desc",
        duration=None,
        filter="for_ios",
        offset=None,
        req_auth=True,
    ):
        # type: (str, str, Optional[str], str, Optional[Union[int, str]], bool) -> ParsedJson
        url = "%s/v1/search/user" % self.hosts
        params = {
            "word": word,
            "sort": sort,
            "filter": filter,
        }  # type: Dict[str, Any]
        if duration:
            params["duration"] = duration
        if offset:
            params["offset"] = offset
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 作品收藏详情
    def illust_bookmark_detail(self, illust_id, req_auth=True):
        # type: (Union[int, str], bool) -> ParsedJson
        url = "%s/v2/illust/bookmark/detail" % self.hosts
        params = {
            "illust_id": illust_id,
        }
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 新增收藏
    def illust_bookmark_add(
        self, illust_id, restrict="public", tags=None, req_auth=True
    ):
        # type: (Union[int, str], str, Optional[Union[str, List[str]]], bool) -> ParsedJson
        url = "%s/v2/illust/bookmark/add" % self.hosts
        data = {
            "illust_id": illust_id,
            "restrict": restrict,
        }
        if isinstance(tags, list):
            tags = " ".join(str(tag) for tag in tags)
        if tags is not None:
            data["tags[]"] = tags

        r = self.no_auth_requests_call("POST", url, data=data, req_auth=req_auth)
        return self.parse_result(r)

    # 删除收藏
    def illust_bookmark_delete(self, illust_id, req_auth=True):
        # type: (Union[int, str], bool) -> ParsedJson
        url = "%s/v1/illust/bookmark/delete" % self.hosts
        data = {
            "illust_id": illust_id,
        }
        r = self.no_auth_requests_call("POST", url, data=data, req_auth=req_auth)
        return self.parse_result(r)

    # 关注用户
    def user_follow_add(self, user_id, restrict="public", req_auth=True):
        # type: (Union[int, str], str, bool) -> ParsedJson
        url = "%s/v1/user/follow/add" % self.hosts
        data = {"user_id": user_id, "restrict": restrict}
        r = self.no_auth_requests_call("POST", url, data=data, req_auth=req_auth)
        return self.parse_result(r)

    # 取消关注用户
    def user_follow_delete(self, user_id, req_auth=True):
        # type: (Union[int, str], bool) -> ParsedJson
        url = "%s/v1/user/follow/delete" % self.hosts
        data = {"user_id": user_id}
        r = self.no_auth_requests_call("POST", url, data=data, req_auth=req_auth)
        return self.parse_result(r)

    # 用户收藏标签列表
    def user_bookmark_tags_illust(self, restrict="public", offset=None, req_auth=True):
        # type: (str, Optional[Union[int, str]], bool) -> ParsedJson
        url = "%s/v1/user/bookmark-tags/illust" % self.hosts
        params = {
            "restrict": restrict,
        }  # type: Dict[str, Any]
        if offset:
            params["offset"] = offset
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # Following用户列表
    def user_following(self, user_id, restrict="public", offset=None, req_auth=True):
        # type: (Union[int, str], str, Optional[Union[int, str]], bool) -> ParsedJson
        url = "%s/v1/user/following" % self.hosts
        params = {
            "user_id": user_id,
            "restrict": restrict,
        }
        if offset:
            params["offset"] = offset

        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # Followers用户列表
    def user_follower(self, user_id, filter="for_ios", offset=None, req_auth=True):
        # type: (Union[int, str], str, Optional[Union[int, str]], bool) -> ParsedJson
        url = "%s/v1/user/follower" % self.hosts
        params = {
            "user_id": user_id,
            "filter": filter,
        }
        if offset:
            params["offset"] = offset

        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 好P友
    def user_mypixiv(self, user_id, offset=None, req_auth=True):
        # type: (Union[int, str], Optional[Union[int, str]], bool) -> ParsedJson
        url = "%s/v1/user/mypixiv" % self.hosts
        params = {
            "user_id": user_id,
        }
        if offset:
            params["offset"] = offset

        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 黑名单用户
    def user_list(self, user_id, filter="for_ios", offset=None, req_auth=True):
        # type: (Union[int, str], str, Optional[Union[int, str]], bool) -> ParsedJson
        url = "%s/v2/user/list" % self.hosts
        params = {
            "user_id": user_id,
            "filter": filter,
        }
        if offset:
            params["offset"] = offset

        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 获取ugoira信息
    def ugoira_metadata(self, illust_id, req_auth=True):
        # type: (Union[int, str], bool) -> ParsedJson
        url = "%s/v1/ugoira/metadata" % self.hosts
        params = {
            "illust_id": illust_id,
        }

        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 用户小说列表
    def user_novels(self, user_id, filter="for_ios", offset=None, req_auth=True):
        # type: (Union[int, str], str, Optional[Union[int, str]], bool) -> ParsedJson
        url = "%s/v1/user/novels" % self.hosts
        params = {
            "user_id": user_id,
            "filter": filter,
        }
        if offset:
            params["offset"] = offset
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 小说系列详情
    def novel_series(self, series_id, filter="for_ios", last_order=None, req_auth=True):
        # type: (Union[int, str], str, Optional[str], bool) -> ParsedJson
        url = "%s/v2/novel/series" % self.hosts
        params = {
            "series_id": series_id,
            "filter": filter,
        }
        if last_order:
            params["last_order"] = last_order
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 小说详情
    def novel_detail(self, novel_id, req_auth=True):
        # type: (Union[int, str], bool) -> ParsedJson
        url = "%s/v2/novel/detail" % self.hosts
        params = {
            "novel_id": novel_id,
        }

        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 小说正文
    def novel_text(self, novel_id, req_auth=True):
        # type: (Union[int, str], bool) -> ParsedJson
        url = "%s/v1/novel/text" % self.hosts
        params = {
            "novel_id": novel_id,
        }

        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 大家的新作
    # content_type: [illust, manga]
    def illust_new(
        self, content_type="illust", filter="for_ios", max_illust_id=None, req_auth=True
    ):
        # type: (str, str, Optional[Union[int, str]], bool) -> ParsedJson
        url = "%s/v1/illust/new" % self.hosts
        params = {
            "content_type": content_type,
            "filter": filter,
        }  # type: Dict[str, Any]
        if max_illust_id:
            params["max_illust_id"] = max_illust_id
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 特辑详情 (无需登录，调用Web API)
    def showcase_article(self, showcase_id):
        # type: (Union[int, str]) -> ParsedJson
        url = "https://www.pixiv.net/ajax/showcase/article"
        # Web API，伪造Chrome的User-Agent
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
            + "(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Referer": "https://www.pixiv.net",
        }
        params = {
            "article_id": showcase_id,
        }

        r = self.no_auth_requests_call(
            "GET", url, headers=headers, params=params, req_auth=False
        )
        return self.parse_result(r)
