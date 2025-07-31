# To keep code compatibility with previous versions:
# ruff: noqa: A002: Function argument `filter` is shadowing a Python builtin
# To keep code compatibility with previous versions:
# ruff: noqa: ARG002: Unused method argument: `req_auth`

from __future__ import annotations

import datetime as dt
import re
import urllib.parse as up
from typing import Any, Literal, Union

try:
    # Python>=3.10
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias

from requests.structures import CaseInsensitiveDict

from . import models
from .api import BasePixivAPI
from .models import ModelT
from .utils import ParamDict, ParsedJson, PixivError, Response

# from typeguard import typechecked
_FILTER: TypeAlias = Literal["for_ios", ""]
_TYPE: TypeAlias = Literal["illust", "manga", ""]
_RESTRICT: TypeAlias = Literal["public", "private", ""]
_CONTENT_TYPE: TypeAlias = Literal["illust", "manga", ""]
_MODE: TypeAlias = Literal[
    "day",
    "week",
    "month",
    "day_male",
    "day_female",
    "week_original",
    "week_rookie",
    "day_manga",
    "day_r18",
    "day_male_r18",
    "day_female_r18",
    "week_r18",
    "week_r18g",
    "",
]
_SEARCH_TARGET: TypeAlias = Literal[
    "partial_match_for_tags", "exact_match_for_tags", "title_and_caption", "keyword", ""
]
_SORT: TypeAlias = Literal["date_desc", "date_asc", "popular_desc", ""]
_DURATION: TypeAlias = Literal[
    "within_last_day", "within_last_week", "within_last_month", "", None
]
_BOOL: TypeAlias = Literal["true", "false"]

DateOrStr = Union[dt.date, str]


# App-API (6.x - app-api.pixiv.net)
# noinspection PyShadowingBuiltins
# @typechecked
class AppPixivAPI(BasePixivAPI):
    def __init__(self, **requests_kwargs: Any) -> None:
        """Initialize requests kwargs if need be"""
        super().__init__(**requests_kwargs)

    # noinspection HttpUrlsUsage
    def set_api_proxy(self, proxy_hosts: str = "http://app-api.pixivlite.com") -> None:
        """Set proxy hosts: eg pixivlite.com"""
        self.hosts = proxy_hosts

    # Check auth and set BearerToken to headers
    def no_auth_requests_call(
        self,
        method: str,
        url: str,
        headers: ParamDict = None,
        params: ParamDict = None,
        data: ParamDict = None,
        req_auth: bool = True,
    ) -> Response:
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
        self.require_auth()
        headers_["Authorization"] = f"Bearer {self.access_token}"
        return self.requests_call(method, url, headers_, params, data)

    def parse_result(self, res: Response) -> ParsedJson:
        try:
            return self.parse_json(res.text)
        except Exception as e:  # noqa: BLE001
            msg = f"parse_json() error: {e}"
            raise PixivError(msg, header=res.headers, body=res.text) from None

    def _load_result(self, res: Response, model: type[ModelT], /) -> ModelT:
        json_data = self.parse_result(res)

        try:
            return model.model_validate(json_data)
        except Exception as e:
            msg = f"_load_result() error: {e}"
            raise PixivError(msg, header=res.headers, body=json_data) from e

    @classmethod
    def _load_model(cls, data: ParsedJson, model: type[ModelT], /) -> ModelT:
        try:
            return model.model_validate(data)
        except Exception as e:
            msg = f"_load_model() error: {e}"
            raise PixivError(msg, body=data) from e

    @classmethod
    def format_bool(cls, bool_value: bool | str | None) -> _BOOL:
        if isinstance(bool_value, bool):
            return "true" if bool_value else "false"
        if bool_value in {"true", "True"}:
            return "true"
        return "false"

    @classmethod
    def _format_date(cls, date: DateOrStr) -> str:
        if isinstance(date, dt.datetime):
            return date.strftime("%Y-%m-%d")
        # `Pixiv` raises an error if the date is not in the format `YYYY-MM-DD`
        assert isinstance(date, str)
        return date

    # 返回翻页用参数
    @classmethod
    def parse_qs(cls, next_url: str | None) -> dict[str, Any] | None:
        if next_url is None:
            return None

        result_qs: dict[str, str | list[str]] = {}
        query = up.urlparse(next_url).query

        for key, value in up.parse_qs(query).items():
            # merge seed_illust_ids[] liked PHP params to array
            if "[" in key and key.endswith("]"):
                # keep the origin sequence, just ignore array length
                result_qs[key.split("[")[0]] = value
            else:
                result_qs[key] = value[-1]

        return result_qs

    # 用户详情
    def user_detail(
        self,
        user_id: int | str,
        filter: _FILTER = "for_ios",
        req_auth: bool = True,
    ) -> models.UserInfoDetailed:
        url = f"{self.hosts}/v1/user/detail"
        params = {
            "user_id": user_id,
            "filter": filter,
        }
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self._load_result(r, models.UserInfoDetailed)

    # 用户作品列表
    ## type: [illust, manga]
    def user_illusts(
        self,
        user_id: int | str,
        type: _TYPE = "illust",
        filter: _FILTER = "for_ios",
        offset: int | str | None = None,
        req_auth: bool = True,
    ) -> models.UserIllustrations:
        url = f"{self.hosts}/v1/user/illusts"
        params = {
            "user_id": user_id,
            "filter": filter,
        }
        if type is not None:
            params["type"] = type
        if offset:
            params["offset"] = offset
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self._load_result(r, models.UserIllustrations)

    # 用户收藏作品列表
    # tag: 从 user_bookmark_tags_illust 获取的收藏标签
    def user_bookmarks_illust(
        self,
        user_id: int | str,
        restrict: _RESTRICT = "public",
        filter: _FILTER = "for_ios",
        max_bookmark_id: int | str | None = None,
        tag: str | None = None,
        req_auth: bool = True,
    ) -> models.UserBookmarksIllustrations:
        url = f"{self.hosts}/v1/user/bookmarks/illust"
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
        return self._load_result(r, models.UserBookmarksIllustrations)

    # 用户收藏小说列表
    def user_bookmarks_novel(
        self,
        user_id: int | str,
        restrict: _RESTRICT = "public",
        filter: _FILTER = "for_ios",
        max_bookmark_id: int | str | None = None,
        tag: str | None = None,
        req_auth: bool = True,
    ) -> models.UserBookmarksNovel:
        url = f"{self.hosts}/v1/user/bookmarks/novel"
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
        return self._load_result(r, models.UserBookmarksNovel)

    def user_related(
        self,
        seed_user_id: int | str,
        filter: _FILTER = "for_ios",
        offset: int | str | None = None,
        req_auth: bool = True,
    ) -> ParsedJson:
        url = f"{self.hosts}/v1/user/related"
        params = {
            "filter": filter,
            # Pixiv warns to put seed_user_id at the end -> put offset here
            "offset": offset if offset else 0,
            "seed_user_id": seed_user_id,
        }
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    def user_recommended(
        self,
        filter: _FILTER = "for_ios",
        offset: int | str | None = None,
        req_auth: bool = True,
    ) -> ParsedJson:
        url = f"{self.hosts}/v1/user/recommended"
        params = {
            "filter": filter,
        }
        if offset:
            params["offset"] = offset  # type: ignore[assignment]

        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 关注用户的新作
    # restrict: [public, private]
    def illust_follow(
        self,
        restrict: _RESTRICT = "public",
        offset: int | str | None = None,
        req_auth: bool = True,
    ) -> ParsedJson:
        url = f"{self.hosts}/v2/illust/follow"
        params: dict[str, str | int] = {
            "restrict": restrict,
        }
        if offset:
            params["offset"] = offset
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 作品详情 (类似PAPI.works(),iOS中未使用)
    def illust_detail(self, illust_id: int | str, req_auth: bool = True) -> ParsedJson:
        url = f"{self.hosts}/v1/illust/detail"
        params = {
            "illust_id": illust_id,
        }
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 作品评论
    def illust_comments(
        self,
        illust_id: int | str,
        offset: int | str | None = None,
        include_total_comments: str | bool | None = None,
        req_auth: bool = True,
    ) -> ParsedJson:
        url = f"{self.hosts}/v1/illust/comments"
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
        illust_id: int | str,
        filter: _FILTER = "for_ios",
        seed_illust_ids: int | str | list[str] | None = None,
        offset: int | str | None = None,
        viewed: str | list[str] | None = None,
        req_auth: bool = True,
    ) -> ParsedJson:
        url = f"{self.hosts}/v2/illust/related"
        params: dict[str, Any] = {
            "illust_id": illust_id,
            "filter": filter,
            "offset": offset,
        }
        if isinstance(seed_illust_ids, str):
            params["seed_illust_ids[]"] = [seed_illust_ids]
        elif isinstance(seed_illust_ids, list):
            params["seed_illust_ids[]"] = seed_illust_ids
        if isinstance(viewed, str):
            params["viewed[]"] = [viewed]
        elif isinstance(viewed, list):
            params["viewed[]"] = viewed
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 插画推荐 (Home - Main)
    # content_type: [illust, manga]
    def illust_recommended(
        self,
        content_type: _CONTENT_TYPE = "illust",
        include_ranking_label: bool | str = True,
        filter: _FILTER = "for_ios",
        max_bookmark_id_for_recommend: int | str | None = None,
        min_bookmark_id_for_recent_illust: int | str | None = None,
        offset: int | str | None = None,
        include_ranking_illusts: str | bool | None = None,
        bookmark_illust_ids: str | list[int | str] | None = None,
        include_privacy_policy: str | list[int | str] | None = None,
        viewed: str | list[str] | None = None,
        req_auth: bool = True,
    ) -> ParsedJson:
        if req_auth:
            url = f"{self.hosts}/v1/illust/recommended"
        else:
            url = f"{self.hosts}/v1/illust/recommended-nologin"
        params: dict[str, Any] = {
            "content_type": content_type,
            "include_ranking_label": self.format_bool(include_ranking_label),
            "filter": filter,
        }
        if max_bookmark_id_for_recommend:
            params["max_bookmark_id_for_recommend"] = max_bookmark_id_for_recommend
        if min_bookmark_id_for_recent_illust:
            params["min_bookmark_id_for_recent_illust"] = (
                min_bookmark_id_for_recent_illust
            )
        if offset:
            params["offset"] = offset
        if include_ranking_illusts:
            params["include_ranking_illusts"] = self.format_bool(
                include_ranking_illusts
            )
        if isinstance(viewed, str):
            params["viewed[]"] = [viewed]
        elif isinstance(viewed, list):
            params["viewed[]"] = viewed

        if not req_auth and isinstance(bookmark_illust_ids, (str, list)):
            params["bookmark_illust_ids"] = (
                ",".join(str(iid) for iid in bookmark_illust_ids)
                if isinstance(bookmark_illust_ids, list)
                else bookmark_illust_ids
            )

        if include_privacy_policy:
            params["include_privacy_policy"] = include_privacy_policy

        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 小说作品评论
    def novel_comments(
        self,
        novel_id: int | str,
        offset: int | str | None = None,
        include_total_comments: str | bool | None = None,
        req_auth: bool = True,
    ) -> models.NovelComments:
        url = f"{self.hosts}/v1/novel/comments"
        params = {
            "novel_id": novel_id,
        }
        if offset:
            params["offset"] = offset
        if include_total_comments:
            params["include_total_comments"] = self.format_bool(include_total_comments)
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self._load_result(r, models.NovelComments)

    # 小说推荐
    def novel_recommended(
        self,
        include_ranking_label: bool | str = True,
        filter: _FILTER = "for_ios",
        offset: int | str | None = None,
        include_ranking_novels: str | bool | None = None,
        already_recommended: str | list[str] | None = None,
        max_bookmark_id_for_recommend: int | str | None = None,
        include_privacy_policy: str | list[int | str] | None = None,
        req_auth: bool = True,
    ) -> ParsedJson:
        url = f"{self.hosts}/v1/novel/recommended"
        params: dict[str, Any] = {
            "include_ranking_label": self.format_bool(include_ranking_label),
            "filter": filter,
        }
        if offset:
            params["offset"] = offset
        if include_ranking_novels:
            params["include_ranking_novels"] = self.format_bool(include_ranking_novels)
        if max_bookmark_id_for_recommend:
            params["max_bookmark_id_for_recommend"] = max_bookmark_id_for_recommend
        if already_recommended:
            if isinstance(already_recommended, str):
                params["already_recommended"] = already_recommended
            elif isinstance(already_recommended, list):
                params["already_recommended"] = ",".join(
                    str(iid) for iid in already_recommended
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
        self,
        mode: _MODE = "day",
        filter: _FILTER = "for_ios",
        date: DateOrStr | None = None,
        offset: int | str | None = None,
        req_auth: bool = True,
    ) -> ParsedJson:
        url = f"{self.hosts}/v1/illust/ranking"
        params: dict[str, Any] = {
            "mode": mode,
            "filter": filter,
        }
        if date:
            params["date"] = self._format_date(date)
        if offset:
            params["offset"] = offset
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 趋势标签 (Search - tags)
    def trending_tags_illust(
        self, filter: _FILTER = "for_ios", req_auth: bool = True
    ) -> ParsedJson:
        url = f"{self.hosts}/v1/trending-tags/illust"
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
    # search_ai_type: 0|1 (0: 过滤AI生成作品, 1: 显示AI生成作品)
    # start_date, end_date: '2020-07-01'
    def search_illust(
        self,
        word: str,
        search_target: _SEARCH_TARGET = "partial_match_for_tags",
        sort: _SORT = "date_desc",
        duration: _DURATION = None,
        start_date: DateOrStr | None = None,
        end_date: DateOrStr | None = None,
        filter: _FILTER = "for_ios",
        search_ai_type: Literal[0, 1] | None = None,
        offset: int | str | None = None,
        req_auth: bool = True,
    ) -> models.SearchIllustrations:
        url = f"{self.hosts}/v1/search/illust"
        params: dict[str, Any] = {
            "word": word,
            "search_target": search_target,
            "sort": sort,
            "filter": filter,
        }
        if start_date:
            params["start_date"] = self._format_date(start_date)
        if end_date:
            params["end_date"] = self._format_date(end_date)
        if duration:
            params["duration"] = duration
        if search_ai_type:
            params["search_ai_type"] = search_ai_type
        if offset:
            params["offset"] = offset
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self._load_result(r, models.SearchIllustrations)

    # 搜索小说 (Search Novel)
    # search_target - 搜索类型
    #   partial_match_for_tags  - 标签部分一致
    #   exact_match_for_tags    - 标签完全一致
    #   text                    - 正文
    #   keyword                 - 关键词
    # sort: [date_desc, date_asc]
    # search_ai_type: 0|1 (0: 过滤AI生成作品, 1: 显示AI生成作品)
    # start_date/end_date: 2020-06-01
    def search_novel(
        self,
        word: str,
        search_target: _SEARCH_TARGET = "partial_match_for_tags",
        sort: _SORT = "date_desc",
        merge_plain_keyword_results: _BOOL = "true",
        include_translated_tag_results: _BOOL = "true",
        start_date: DateOrStr | None = None,
        end_date: DateOrStr | None = None,
        filter: str | None = None,
        search_ai_type: Literal[0, 1] | None = None,
        offset: int | str | None = None,
        req_auth: bool = True,
    ) -> models.SearchNovel:
        url = f"{self.hosts}/v1/search/novel"
        params: dict[str, Any] = {
            "word": word,
            "search_target": search_target,
            "merge_plain_keyword_results": merge_plain_keyword_results,
            "include_translated_tag_results": include_translated_tag_results,
            "sort": sort,
            "filter": filter,
        }
        if start_date:
            params["start_date"] = self._format_date(start_date)
        if end_date:
            params["end_date"] = self._format_date(end_date)
        if search_ai_type:
            params["search_ai_type"] = search_ai_type
        if offset:
            params["offset"] = offset
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self._load_result(r, models.SearchNovel)

    def search_user(
        self,
        word: str,
        sort: _SORT = "date_desc",
        duration: _DURATION = None,
        filter: _FILTER = "for_ios",
        offset: int | str | None = None,
        req_auth: bool = True,
    ) -> ParsedJson:
        url = f"{self.hosts}/v1/search/user"
        params: dict[str, Any] = {
            "word": word,
            "sort": sort,
            "filter": filter,
        }
        if duration:
            params["duration"] = duration
        if offset:
            params["offset"] = offset
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 作品收藏详情
    def illust_bookmark_detail(
        self, illust_id: int | str, req_auth: bool = True
    ) -> ParsedJson:
        url = f"{self.hosts}/v2/illust/bookmark/detail"
        params = {
            "illust_id": illust_id,
        }
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 新增收藏
    def illust_bookmark_add(
        self,
        illust_id: int | str,
        restrict: _RESTRICT = "public",
        tags: str | list[str] | None = None,
        req_auth: bool = True,
    ) -> ParsedJson:
        url = f"{self.hosts}/v2/illust/bookmark/add"
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
    def illust_bookmark_delete(
        self, illust_id: int | str, req_auth: bool = True
    ) -> ParsedJson:
        url = f"{self.hosts}/v1/illust/bookmark/delete"
        data = {
            "illust_id": illust_id,
        }
        r = self.no_auth_requests_call("POST", url, data=data, req_auth=req_auth)
        return self.parse_result(r)

    # 关注用户
    def user_follow_add(
        self,
        user_id: int | str,
        restrict: _RESTRICT = "public",
        req_auth: bool = True,
    ) -> ParsedJson:
        url = f"{self.hosts}/v1/user/follow/add"
        data = {"user_id": user_id, "restrict": restrict}
        r = self.no_auth_requests_call("POST", url, data=data, req_auth=req_auth)
        return self.parse_result(r)

    # 取消关注用户
    def user_follow_delete(
        self, user_id: int | str, req_auth: bool = True
    ) -> ParsedJson:
        url = f"{self.hosts}/v1/user/follow/delete"
        data = {"user_id": user_id}
        r = self.no_auth_requests_call("POST", url, data=data, req_auth=req_auth)
        return self.parse_result(r)

    # 设置用户选项中是否展现AI生成作品
    def user_edit_ai_show_settings(
        self, setting: _BOOL, req_auth: bool = True
    ) -> ParsedJson:
        url = f"{self.hosts}/v1/user/ai-show-settings/edit"
        data = {"show_ai": setting}
        r = self.no_auth_requests_call("POST", url, data=data, req_auth=req_auth)
        return self.parse_result(r)

    # 用户收藏标签列表
    def user_bookmark_tags_illust(
        self,
        user_id: int | str,
        restrict: _RESTRICT = "public",
        offset: int | str | None = None,
        req_auth: bool = True,
    ) -> ParsedJson:
        url = f"{self.hosts}/v1/user/bookmark-tags/illust"
        params: dict[str, Any] = {
            "user_id": user_id,
            "restrict": restrict,
        }
        if offset:
            params["offset"] = offset
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # Following用户列表
    def user_following(
        self,
        user_id: int | str,
        restrict: _RESTRICT = "public",
        offset: int | str | None = None,
        req_auth: bool = True,
    ) -> models.UserFollowing:
        url = f"{self.hosts}/v1/user/following"
        params = {
            "user_id": user_id,
            "restrict": restrict,
        }
        if offset:
            params["offset"] = offset

        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self._load_result(r, models.UserFollowing)

    # Followers用户列表
    def user_follower(
        self,
        user_id: int | str,
        filter: _FILTER = "for_ios",
        offset: int | str | None = None,
        req_auth: bool = True,
    ) -> ParsedJson:
        url = f"{self.hosts}/v1/user/follower"
        params = {
            "user_id": user_id,
            "filter": filter,
        }
        if offset:
            params["offset"] = offset

        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 好P友
    def user_mypixiv(
        self,
        user_id: int | str,
        offset: int | str | None = None,
        req_auth: bool = True,
    ) -> ParsedJson:
        url = f"{self.hosts}/v1/user/mypixiv"
        params = {
            "user_id": user_id,
        }
        if offset:
            params["offset"] = offset

        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 黑名单用户
    def user_list(
        self,
        user_id: int | str,
        filter: _FILTER = "for_ios",
        offset: int | str | None = None,
        req_auth: bool = True,
    ) -> ParsedJson:
        url = f"{self.hosts}/v2/user/list"
        params = {
            "user_id": user_id,
            "filter": filter,
        }
        if offset:
            params["offset"] = offset

        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 获取ugoira信息
    def ugoira_metadata(
        self, illust_id: int | str, req_auth: bool = True
    ) -> ParsedJson:
        url = f"{self.hosts}/v1/ugoira/metadata"
        params = {
            "illust_id": illust_id,
        }

        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 用户小说列表
    def user_novels(
        self,
        user_id: int | str,
        filter: _FILTER = "for_ios",
        offset: int | str | None = None,
        req_auth: bool = True,
    ) -> models.UserNovels:
        url = f"{self.hosts}/v1/user/novels"
        params = {
            "user_id": user_id,
            "filter": filter,
        }
        if offset:
            params["offset"] = offset
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self._load_result(r, models.UserNovels)

    # 小说系列详情
    def novel_series(
        self,
        series_id: int | str,
        filter: _FILTER = "for_ios",
        last_order: str | None = None,
        req_auth: bool = True,
    ) -> ParsedJson:
        url = f"{self.hosts}/v2/novel/series"
        params = {
            "series_id": series_id,
            "filter": filter,
        }
        if last_order:
            params["last_order"] = last_order
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 小说详情
    def novel_detail(
        self,
        novel_id: int | str,
        req_auth: bool = True,
    ) -> models.NovelInfo:
        url = f"{self.hosts}/v2/novel/detail"
        params = {
            "novel_id": novel_id,
        }

        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        response_json = self.parse_result(r)
        return self._load_model(response_json["novel"], models.NovelInfo)

    def novel_new(
        self,
        filter: _FILTER = "for_ios",
        max_novel_id: int | str | None = None,
        req_auth: bool = True,
    ) -> ParsedJson:
        url = f"{self.hosts}/v1/novel/new"
        params: dict[str, Any] = {
            "filter": filter,
        }
        if max_novel_id:
            params["max_novel_id"] = max_novel_id
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 正在关注的用户的新小说
    # restrict: [public, private, all]
    def novel_follow(
        self,
        restrict: _RESTRICT = "public",
        offset: int | None = None,
        req_auth: bool = True,
    ) -> ParsedJson:
        url = f"{self.hosts}/v1/novel/follow"
        params: dict[str, Any] = {"restrict": restrict, "offset": offset}
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 小说 (webview)
    #  raw=True, return html content directly
    def webview_novel(
        self,
        novel_id: int | str,
        raw: bool = False,
        req_auth: bool = True,
    ) -> models.WebviewNovel | str:
        """使用AJAX API获取小说内容（按照TypeScript代码思路）"""
        
        # 构建AJAX URL - 注意要用www而不是app-api
        if "app-api" in self.hosts:
            base_url = self.hosts.replace("app-api", "www")
        else:
            base_url = self.hosts
        
        url = f"{base_url}/ajax/novel/{novel_id}"
        
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': f'{base_url}/novel/show.php?id={novel_id}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
        }
        
        
        # 添加随机延迟，避免被检测
        import time
        import random
        time.sleep(random.uniform(1, 3))
        r = self.no_auth_requests_call("GET", url, headers=headers, req_auth=req_auth)
        if raw:
            return r.text
        
        try:
            # 使用现有的parse_result方法
            json_data = self.parse_result(r)
            print(f"🔍 解析成功，数据keys: {list(json_data.keys())}")
            
            # 检查API错误
            if 'error' in json_data and json_data['error']:
                error_msg = json_data.get('message', '未知错误')
                raise PixivError(f"API错误: {error_msg}")
            
            # 按照TS代码，数据在body中
            if 'body' not in json_data:
                msg = f"AJAX API响应格式不正确: {list(json_data.keys())}"
                raise PixivError(msg, header=r.headers, body=r.text)
            
            novel_data = json_data['body']
            print(f"获取到body数据，类型: {type(novel_data)}")
            print(f"body数据keys: {list(novel_data.keys()) if hasattr(novel_data, 'keys') else 'No keys'}")
            
            if not novel_data:
                raise PixivError("API返回空数据")
            
            # 直接返回原始数据，避免模型验证问题
            if raw:
                return novel_data
        except PixivError:
            raise
        except Exception as e:
            msg = f"处理AJAX响应时出错: {e}"
            raise PixivError(msg, header=r.headers, body=r.text) from e

    # 小说正文 (deprecated)
    def novel_text(
        self, novel_id: int | str, req_auth: bool = True
    ) -> models.WebviewNovel:
        # /v1/novel/text no longer exist
        json_obj = self.webview_novel(novel_id=novel_id, raw=False)
        assert isinstance(json_obj, models.WebviewNovel)
        json_obj.novel_text = json_obj.text  # type: ignore[attr-defined]
        return json_obj

    # 大家的新作
    # content_type: [illust, manga]
    def illust_new(
        self,
        content_type: _CONTENT_TYPE = "illust",
        filter: _FILTER = "for_ios",
        max_illust_id: int | str | None = None,
        req_auth: bool = True,
    ) -> ParsedJson:
        url = f"{self.hosts}/v1/illust/new"
        params: dict[str, Any] = {
            "content_type": content_type,
            "filter": filter,
        }
        if max_illust_id:
            params["max_illust_id"] = max_illust_id
        r = self.no_auth_requests_call("GET", url, params=params, req_auth=req_auth)
        return self.parse_result(r)

    # 特辑详情 (无需登录,调用Web API)
    def showcase_article(self, showcase_id: int | str) -> ParsedJson:
        url = "https://www.pixiv.net/ajax/showcase/article"
        # Web API, 伪造Chrome的User-Agent
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
            ),
            "Referer": "https://www.pixiv.net",
        }
        params = {
            "article_id": showcase_id,
        }

        r = self.no_auth_requests_call(
            "GET", url, headers=headers, params=params, req_auth=False
        )
        return self.parse_result(r)
