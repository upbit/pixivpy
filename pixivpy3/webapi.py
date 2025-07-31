from __future__ import annotations

import json
from typing import Any, TypeVar, Type, Union, Dict

import httpx
from httpx import Headers, QueryParams, RequestError
from httpx import Response as HttpxResponse

from .utils import PixivError
from .web_models import (
    BaseWebModel,
    BaseAjaxResponse,
    WebAjaxApiError,
    WebUserInfoFull,
    WebFollowingUser,
    WebFollowersUser,
    WebUserInfoShort,
    WebUserProfileAll,
    WebNovelSeriesInfo,
    WebNovelInfoFull,
)

# Base URL for Pixiv Ajax API
AJAX_BASE_URL = "https://www.pixiv.net/ajax"

# 定义泛型类型T，限定为BaseWebModel的子类
T = TypeVar("T", bound=BaseWebModel)
ResponseT = TypeVar("ResponseT", bound=BaseAjaxResponse)

# 定义API结果类型，可以是成功结果或错误结果
ApiResult = Union[T, WebAjaxApiError]


class WebPixivAPI:
    """
    API class for interacting with Pixiv's Web Ajax endpoints.

    Requires authentication via cookies (specifically PHPSESSID).
    Uses httpx for both synchronous and asynchronous requests.
    """

    def __init__(
        self,
        PHPSESSID: str | None = None,
        user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        timeout: float = 30.0,
        proxies: dict | str | None = None,
        **httpx_kwargs: Any,
    ) -> None:
        """
        Initialize WebPixivAPI.

        Args:
            PHPSESSID: The PHPSESSID cookie value obtained after logging in via browser.
            user_agent: The User-Agent string to use for requests.
            timeout: Default timeout for HTTP requests in seconds.
            proxies: Proxies configuration for httpx.
            **httpx_kwargs: Additional keyword arguments passed to httpx clients.
        """
        self.PHPSESSID = PHPSESSID
        self.base_headers = Headers(
            {
                "User-Agent": user_agent,
                "Referer": "https://www.pixiv.net/",
            }
        )
        self.timeout = timeout
        self.httpx_kwargs = httpx_kwargs
        self.proxies = proxies

        # Initialize httpx clients
        self._client: httpx.Client | None = None
        self._async_client: httpx.AsyncClient | None = None

    def _get_client(self) -> httpx.Client:
        """Get or initialize the synchronous httpx client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.Client(
                base_url=AJAX_BASE_URL,
                headers=self.base_headers,
                timeout=self.timeout,
                mounts=self.proxies,  # Corrected parameter name
                cookies=self._get_cookies(),
                **self.httpx_kwargs,
            )
        return self._client

    def _get_async_client(self) -> httpx.AsyncClient:
        """Get or initialize the asynchronous httpx client."""
        if self._async_client is None or self._async_client.is_closed:
            self._async_client = httpx.AsyncClient(
                base_url=AJAX_BASE_URL,
                headers=self.base_headers,
                timeout=self.timeout,
                mounts=self.proxies,  # Corrected parameter name
                cookies=self._get_cookies(),
                **self.httpx_kwargs,
            )
        return self._async_client

    def _get_cookies(self) -> Dict[str, str]:
        """Return cookies dictionary based on PHPSESSID."""
        return {"PHPSESSID": self.PHPSESSID} if self.PHPSESSID else {}

    def set_auth(self, PHPSESSID: str) -> None:
        """Set the PHPSESSID for authentication."""
        self.PHPSESSID = PHPSESSID
        # Re-initialize clients with new cookies if they exist
        if self._client is not None and not self._client.is_closed:
            self._client.cookies = httpx.Cookies(self._get_cookies())
        if self._async_client is not None and not self._async_client.is_closed:
            self._async_client.cookies = httpx.Cookies(self._get_cookies())  # type: ignore

    @staticmethod
    def parse_json(
        response_text: str | bytes,
    ) -> Any:  # Return Any, let Pydantic handle dict
        """
        Parse JSON string. Checks for Pixiv's structured error format
        but does NOT raise PixivError for it anymore, returning the dict instead.
        Raises PixivError only for JSON decoding issues.
        """
        try:
            # Pixiv Ajax responses often have 'error' and 'message' keys on failure
            data: Any = json.loads(response_text)
            # We no longer raise PixivError for {"error": True} here,
            # the calling method will handle it.
            return data  # Return the raw dict/list/etc.
        except (json.JSONDecodeError, TypeError) as e:
            raise PixivError(
                f"Failed to parse JSON response: {e}", body=response_text
            ) from e

    def _request(
        self,
        method: str,
        url: str,
        params: QueryParams | dict | None = None,
        data: Any = None,
        headers: Headers | None = None,
        require_auth: bool = True,
    ) -> HttpxResponse:
        """Performs a synchronous HTTP request."""
        if require_auth and not self.PHPSESSID:
            raise PixivError("Authentication required (PHPSESSID not set).")

        client = self._get_client()
        merged_headers = self.base_headers.copy()
        if headers:
            merged_headers.update(headers)

        try:
            response = client.request(
                method,
                url,
                params=params,
                json=data if method == "POST" else None,  # Assume POST uses JSON body
                headers=merged_headers,
            )
            response.raise_for_status()  # Raise HTTPStatusError for bad responses (4xx or 5xx)
            return response
        except RequestError as e:
            raise PixivError(f"HTTP request failed: {e}", body=e.request) from e
        except Exception as e:
            raise PixivError(
                f"An unexpected error occurred during the request: {e}"
            ) from e

    async def _async_request(
        self,
        method: str,
        url: str,
        params: QueryParams | dict | None = None,
        data: Any = None,
        headers: Headers | None = None,
        require_auth: bool = True,
    ) -> HttpxResponse:
        """Performs an asynchronous HTTP request."""
        if require_auth and not self.PHPSESSID:
            raise PixivError("Authentication required (PHPSESSID not set).")

        client = self._get_async_client()
        merged_headers = self.base_headers.copy()
        if headers:
            merged_headers.update(headers)

        try:
            response = await client.request(
                method,
                url,
                params=params,
                json=data if method == "POST" else None,  # Assume POST uses JSON body
                headers=merged_headers,
            )
            response.raise_for_status()  # Raise HTTPStatusError for bad responses (4xx or 5xx)
            return response
        except RequestError as e:
            raise PixivError(f"HTTP request failed: {e}", body=e.request) from e
        except Exception as e:
            raise PixivError(
                f"An unexpected error occurred during the request: {e}"
            ) from e

    def _parse_and_validate_response(
        self, response: HttpxResponse, body_class: Type[T]
    ) -> ApiResult[T]:
        """
        解析并验证API响应，转换为相应的模型对象或错误对象。

        Args:
            response: HTTP响应对象
            body_class: 用于验证响应体的Pydantic模型类 (必须是 BaseWebModel 的子类)

        Returns:
            成功时返回类型T的实例，失败时返回WebAjaxApiError

        Raises:
            PixivError: JSON解析错误或响应结构不符合预期
        """
        try:
            json_data = self.parse_json(response.content)
        except PixivError as pe:
            pe.header = response.headers
            raise pe

        if not isinstance(json_data, dict):
            raise PixivError(
                "Unexpected API response format (not a dict)",
                body=json_data,
                header=response.headers,
            )

        # 检查是否是错误响应
        if json_data.get("error", False):
            try:
                return WebAjaxApiError.model_validate(json_data)
            except Exception as e:
                raise PixivError(
                    f"Failed to validate error response: {e}",
                    body=json_data,
                    header=response.headers,
                ) from e

        # 成功响应，验证body
        if "body" not in json_data:
            raise PixivError(
                "Unexpected API response format (missing 'body')",
                body=json_data,
                header=response.headers,
            )

        try:
            return body_class.model_validate(json_data["body"])
        except Exception as e:
            raise PixivError(
                f"Failed to validate API response body: {e}",
                body=json_data,
                header=response.headers,
            ) from e

    def _process_response(
        self, response: HttpxResponse, body_class: Type[T]
    ) -> ApiResult[T]:
        """
        统一处理同步API响应，转换为相应的模型对象或错误对象。

        Args:
            response: HTTP响应对象
            body_class: 用于验证响应体的Pydantic模型类 (必须是 BaseWebModel 的子类)

        Returns:
            成功时返回类型T的实例，失败时返回WebAjaxApiError

        Raises:
            PixivError: JSON解析错误或响应结构不符合预期
        """
        return self._parse_and_validate_response(response, body_class)

    async def _async_process_response(
        self, response: HttpxResponse, body_class: Type[T]
    ) -> ApiResult[T]:
        """
        异步版本：统一处理API响应，转换为相应的模型对象或错误对象。

        Args:
            response: HTTP响应对象
            body_class: 用于验证响应体的Pydantic模型类 (必须是 BaseWebModel 的子类)

        Returns:
            成功时返回类型T的实例，失败时返回WebAjaxApiError

        Raises:
            PixivError: JSON解析错误或响应结构不符合预期
        """
        # 解析和验证是同步操作，可以直接调用辅助方法
        return self._parse_and_validate_response(response, body_class)

    def close(self) -> None:
        """Close the synchronous httpx client."""
        if self._client and not self._client.is_closed:
            self._client.close()

    async def aclose(self) -> None:
        """Close the asynchronous httpx client."""
        if self._async_client and not self._async_client.is_closed:
            await self._async_client.aclose()

    # --- User Information ---

    def get_user_info_short(self, user_id: int | str) -> ApiResult[WebUserInfoShort]:
        """
        Get user information in a simplified format. (Corresponds to /ajax/user/{USER_ID})

        Returns:
            成功时返回WebUserInfoShort实例，失败时返回WebAjaxApiError
        Raises:
            PixivError: For network issues, non-2xx HTTP status, JSON parsing errors, or missing auth.
        """
        url = f"/user/{user_id}"
        response = self._request("GET", url, require_auth=True)
        return self._process_response(response, WebUserInfoShort)

    async def async_get_user_info_short(
        self, user_id: int | str
    ) -> ApiResult[WebUserInfoShort]:
        """
        Get user information in a simplified format. (Async) (Corresponds to /ajax/user/{USER_ID})

        Returns:
            成功时返回WebUserInfoShort实例，失败时返回WebAjaxApiError
        Raises:
            PixivError: For network issues, non-2xx HTTP status, JSON parsing errors, or missing auth.
        """
        url = f"/user/{user_id}"
        response = await self._async_request("GET", url, require_auth=True)
        return await self._async_process_response(response, WebUserInfoShort)

    def get_user_info_full(self, user_id: int | str) -> ApiResult[WebUserInfoFull]:
        """
        Get full user information. (Corresponds to /ajax/user/{USER_ID}?full=1)

        Returns:
            成功时返回WebUserInfoFull实例，失败时返回WebAjaxApiError
        Raises:
            PixivError: For network issues, non-2xx HTTP status, JSON parsing errors, or missing auth.
        """
        url = f"/user/{user_id}"
        params = {"full": "1"}
        response = self._request("GET", url, params=params, require_auth=True)
        return self._process_response(response, WebUserInfoFull)

    async def async_get_user_info_full(
        self, user_id: int | str
    ) -> ApiResult[WebUserInfoFull]:
        """
        Get full user information. (Async) (Corresponds to /ajax/user/{USER_ID}?full=1)

        Returns:
            成功时返回WebUserInfoFull实例，失败时返回WebAjaxApiError
        Raises:
            PixivError: For network issues, non-2xx HTTP status, JSON parsing errors, or missing auth.
        """
        url = f"/user/{user_id}"
        params = {"full": "1"}
        response = await self._async_request(
            "GET", url, params=params, require_auth=True
        )
        return await self._async_process_response(response, WebUserInfoFull)

    def get_user_profile_all(self, user_id: int | str) -> ApiResult[WebUserProfileAll]:
        """
        Get user information along with information about artwork posted by the user.
        (Corresponds to /ajax/user/{USER_ID}/profile/all)

        Returns:
            成功时返回WebUserProfileAll实例，失败时返回WebAjaxApiError
        Raises:
            PixivError: For network issues, non-2xx HTTP status, JSON parsing errors, or missing auth.
        """
        url = f"/user/{user_id}/profile/all"
        response = self._request("GET", url, require_auth=True)
        return self._process_response(response, WebUserProfileAll)

    async def async_get_user_profile_all(
        self, user_id: int | str
    ) -> ApiResult[WebUserProfileAll]:
        """
        Get user information along with information about artwork posted by the user. (Async)
        (Corresponds to /ajax/user/{USER_ID}/profile/all)

        Returns:
            成功时返回WebUserProfileAll实例，失败时返回WebAjaxApiError
        Raises:
            PixivError: For network issues, non-2xx HTTP status, JSON parsing errors, or missing auth.
        """
        url = f"/user/{user_id}/profile/all"
        response = await self._async_request("GET", url, require_auth=True)
        return await self._async_process_response(response, WebUserProfileAll)

    def get_user_following(
        self, user_id: int | str, limit: int = 30, offset: int = 0
    ) -> ApiResult[WebFollowingUser]:
        """
        Get the list of users followed by the specified user.
        (Corresponds to /ajax/user/{USER_ID}/following)

        Requires authentication (PHPSESSID).

        Args:
            user_id: The target user ID.
            offset: Starting offset for pagination.
            limit: Number of users to return per page.

        Returns:
            成功时返回WebFollowingUser实例，失败时返回WebAjaxApiError
        Raises:
            PixivError: For network issues, non-2xx HTTP status, JSON parsing errors, or missing auth.
        """
        url = f"/user/{user_id}/following"
        params: Dict[str, Any] = {"rest": "show"}
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit

        response = self._request("GET", url, params=params, require_auth=True)

        return self._process_response(response, WebFollowingUser)

    async def async_get_user_following(
        self, user_id: int | str, limit: int = 30, offset: int = 0
    ) -> ApiResult[WebFollowingUser]:
        """
        Get the list of users followed by the specified user. (Async)
        (Corresponds to /ajax/user/{USER_ID}/following)

        Requires authentication (PHPSESSID).

        Args:
            user_id: The target user ID.
            offset: Starting offset for pagination.
            limit: Number of users to return per page.

        Returns:
            成功时返回WebFollowingUser实例，失败时返回WebAjaxApiError
        Raises:
            PixivError: For network issues, non-2xx HTTP status, JSON parsing errors, or missing auth.
        """
        url = f"/user/{user_id}/following"
        params: Dict[str, Any] = {"rest": "show"}
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit

        response = await self._async_request(
            "GET", url, params=params, require_auth=True
        )

        return self._process_response(response, WebFollowingUser)

    def get_user_followers(
        self, user_id: int | str, limit: int = 30, offset: int = 0
    ) -> WebFollowersUser:
        """
        Get the list of users who follow the specified user.
        (Corresponds to /ajax/user/{USER_ID}/followers)

        Requires authentication (PHPSESSID).

        Args:
            user_id: The target user ID.
            offset: Starting offset for pagination.
            limit: Number of users to return per page.

        Returns:
            WebFollowingUser containing the response data or error information.
        Raises:
            PixivError: For network issues, non-2xx HTTP status, JSON parsing errors, or missing auth.
        """
        url = f"/user/{user_id}/followers"
        params: Dict[str, Any] = {}
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit

        response = self._request("GET", url, params=params, require_auth=True)
        return self._process_response(response, WebFollowersUser)

    async def async_get_user_followers(
        self, user_id: int | str, limit: int = 30, offset: int = 0
    ) -> WebFollowersUser:
        """
        Get the list of users who follow the specified user. (Async)
        (Corresponds to /ajax/user/{USER_ID}/followers)

        Requires authentication (PHPSESSID).

        Args:
            user_id: The target user ID.
            offset: Starting offset for pagination.
            limit: Number of users to return per page.

        Returns:
            WebFollowingUser containing the response data or error information.
        Raises:
            PixivError: For network issues, non-2xx HTTP status, JSON parsing errors, or missing auth.
        """
        url = f"/user/{user_id}/followers"
        params: Dict[str, Any] = {}
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit

        response = await self._async_request(
            "GET", url, params=params, require_auth=True
        )
        return self._process_response(response, WebFollowersUser)

    def get_novel_series_info(
        self, novel_series_id: int | str, language: str | None = "zh"
    ) -> ApiResult[WebNovelSeriesInfo]:
        """
        获取小说系列信息。
        (对应 /ajax/novel/series/{NOVEL_SERIES_ID})

        Args:
            novel_series_id: 小说系列ID
            language: 语言代码，默认为 'zh'

        Returns:
            成功时返回WebNovelSeriesInfo实例，失败时返回WebAjaxApiError
        Raises:
            PixivError: 网络问题、非2xx HTTP状态码、JSON解析错误或缺少认证信息
        """
        url = f"/novel/series/{novel_series_id}"
        params: Dict[str, Any] = {}
        if language is not None:
            params["lang"] = language

        response = self._request("GET", url, params=params, require_auth=False)
        return self._process_response(response, WebNovelSeriesInfo)

    async def async_get_novel_series_info(
        self, novel_series_id: int | str, language: str | None = "zh"
    ) -> ApiResult[WebNovelSeriesInfo]:
        """
        获取小说系列信息。(异步版本)
        (对应 /ajax/novel/series/{NOVEL_SERIES_ID})

        Args:
            novel_series_id: 小说系列ID
            language: 语言代码，默认为 'zh'

        Returns:
            成功时返回WebNovelSeriesInfo实例，失败时返回WebAjaxApiError
        Raises:
            PixivError: 网络问题、非2xx HTTP状态码、JSON解析错误或缺少认证信息
        """
        url = f"/novel/series/{novel_series_id}"
        params: Dict[str, Any] = {}
        if language is not None:
            params["lang"] = language

        response = await self._async_request(
            "GET", url, params=params, require_auth=False
        )
        return await self._async_process_response(response, WebNovelSeriesInfo)

    def get_novel_info(
        self, novel_id: int | str, language: str | None = "zh"
    ) -> ApiResult[WebNovelInfoFull]:
        """
        获取小说信息。
        (对应 /ajax/novel/{NOVEL_ID})

        Args:
            novel_id: 小说ID
            language: 语言代码，默认为 'zh'
        Returns:
            成功时返回WebNovelInfoFull实例(小说的完整信息，包括正文)，失败时返回WebAjaxApiError
        Raises:
            PixivError: 网络问题、非2xx HTTP状态码、JSON解析错误或缺少认证信息
        """
        url = f"/novel/{novel_id}"
        params: Dict[str, Any] = {}
        if language is not None:
            params["lang"] = language

        response = self._request("GET", url, params=params, require_auth=False)
        return self._process_response(response, WebNovelInfoFull)

    # --- Placeholder for more API methods ---
    # Example structure for an endpoint:
    # def get_user_info(self, user_id: int) -> ParsedJson: # Keep old example for reference if needed
    #     url = f"/user/{user_id}"
    #     response = self._request("GET", url, require_auth=False) # Example: this endpoint might not need auth
    #     # TODO: Define and use Pydantic model here
    #     return self.parse_json(response.content)
    #
    # async def async_get_user_info(self, user_id: int) -> ParsedJson:
    #     url = f"/user/{user_id}"
    #     response = await self._async_request("GET", url, require_auth=False)
    #     # TODO: Define and use Pydantic model here
    #     return self.parse_json(response.content)

    def __enter__(self) -> WebPixivAPI:
        self._get_client()  # Ensure client is initialized
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    async def __aenter__(self) -> WebPixivAPI:
        self._get_async_client()  # Ensure async client is initialized
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.aclose()
