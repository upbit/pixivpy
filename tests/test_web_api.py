import pytest
import respx
from httpx import Response
import json

import pytest # Import pytest for raises
import respx
from httpx import Response

from pixivpy3 import PixivError, WebPixivAPI
# Import the new error model and user profile models
from pixivpy3.web_models import (
    WebAjaxApiError,
    WebUserInfoFull,
    WebUserInfoShort,
    WebUserProfileAllBody,
    WebFollowingUserBody, # Added import
)
from tests.fixtures.web_api_data import (
    AJAX_BASE_URL,
    TEST_USER_ID,
    EXAMPLE_USER_INFO_SHORT_RESPONSE,
    EXAMPLE_USER_INFO_FULL_RESPONSE,
)

@pytest.fixture
def web_api() -> WebPixivAPI:
    """Fixture to provide a WebPixivAPI instance for tests."""
    return WebPixivAPI()


@pytest.fixture
def authenticated_web_api() -> WebPixivAPI:
    """Fixture to provide an authenticated WebPixivAPI instance."""
    return WebPixivAPI(PHPSESSID="test_session_id")


@respx.mock
def test_get_user_info_short_success(web_api: WebPixivAPI):
    """Test successful retrieval of short user info (sync) using example data."""
    mock_url = f"{AJAX_BASE_URL}/user/{TEST_USER_ID}"
    # Use the exact example response
    respx.get(mock_url).mock(return_value=Response(200, json=EXAMPLE_USER_INFO_SHORT_RESPONSE))

    result = web_api.get_user_info_short(TEST_USER_ID)

    # Check if the result is the expected user info object, not the error object
    assert isinstance(result, WebUserInfoShort)
    # Check some fields directly on the returned body object
    assert result.user_id == str(TEST_USER_ID) # Model defines it as str
    assert result.name == "haku89"
    assert result.premium is True
    # Access attributes directly on the result (WebUserInfoShort) object
    assert result.is_followed is False
    assert result.accept_request is False


@pytest.mark.asyncio
@respx.mock
async def test_async_get_user_info_short_success(web_api: WebPixivAPI):
    """Test successful retrieval of short user info (async) using example data."""
    mock_url = f"{AJAX_BASE_URL}/user/{TEST_USER_ID}"
     # Use the exact example response
    respx.get(mock_url).mock(return_value=Response(200, json=EXAMPLE_USER_INFO_SHORT_RESPONSE))

    result = await web_api.async_get_user_info_short(TEST_USER_ID)

    # Check if the result is the expected user info object, not the error object
    assert isinstance(result, WebUserInfoShort)
    # Check some fields directly on the returned body object
    assert result.user_id == str(TEST_USER_ID)
    assert result.name == "haku89"
    assert result.premium is True
    # Access attributes directly on the result (WebUserInfoShort) object
    assert result.is_followed is False
    assert result.accept_request is False


@respx.mock
def test_get_user_info_short_api_error(web_api: WebPixivAPI):
    """Test API error during retrieval of short user info (sync)."""
    mock_url = f"{AJAX_BASE_URL}/user/{TEST_USER_ID}"
    mock_error_response_body = {
        "error": True,
        "message": "User not found",
        "body": {}, # Pixiv Ajax often returns empty body on error, include it in mock
    }
    respx.get(mock_url).mock(return_value=Response(200, json=mock_error_response_body))

    # Expect the method to return the WebAjaxApiError model, not raise PixivError
    result = web_api.get_user_info_short(TEST_USER_ID)

    assert isinstance(result, WebAjaxApiError)
    assert result.error is True
    assert result.message == "User not found"
    assert result.body == {} # Check the body passed in the error model


@pytest.mark.asyncio
@respx.mock
async def test_async_get_user_info_short_http_error(web_api: WebPixivAPI):
    """Test HTTP error during retrieval of short user info (async)."""
    mock_url = f"{AJAX_BASE_URL}/user/{TEST_USER_ID}"
    respx.get(mock_url).mock(return_value=Response(404)) # Simulate Not Found

    with pytest.raises(PixivError) as excinfo:
        await web_api.async_get_user_info_short(TEST_USER_ID)
    # Check if the error message indicates an HTTP error (status code)
    assert "404 Not Found" in str(excinfo.value) or "HTTP request failed" in str(excinfo.value)


# --- Tests for get_user_info_full ---

@respx.mock
def test_get_user_info_full_success(web_api: WebPixivAPI):
    """Test successful retrieval of full user info (sync)."""
    mock_url = f"{AJAX_BASE_URL}/user/{TEST_USER_ID}"
    # Use the exact example response for the 'full' endpoint
    respx.get(mock_url, params={"full": "1"}).mock(
        return_value=Response(200, json=EXAMPLE_USER_INFO_FULL_RESPONSE)
    )

    result = web_api.get_user_info_full(TEST_USER_ID)

    assert isinstance(result, WebUserInfoFull)
    assert result.user_id == TEST_USER_ID
    assert result.name == "haku89"
    assert result.following == 349 # Check a field specific to the full response
    assert result.workspace is not None
    assert result.workspace.pc == "RTX 3090+Ryzen5800X"
    assert result.official is False


@pytest.mark.asyncio
@respx.mock
async def test_async_get_user_info_full_success(web_api: WebPixivAPI):
    """Test successful retrieval of full user info (async)."""
    mock_url = f"{AJAX_BASE_URL}/user/{TEST_USER_ID}"
    respx.get(mock_url, params={"full": "1"}).mock(
        return_value=Response(200, json=EXAMPLE_USER_INFO_FULL_RESPONSE)
    )

    result = await web_api.async_get_user_info_full(TEST_USER_ID)

    assert isinstance(result, WebUserInfoFull)
    assert result.user_id == TEST_USER_ID
    assert result.following == 349
    assert result.social is not None
    assert result.social.twitter is not None
    assert result.social.twitter.url == "https://twitter.com/real_haku89"


@respx.mock
def test_get_user_info_full_api_error(web_api: WebPixivAPI):
    """Test API error during retrieval of full user info (sync)."""
    mock_url = f"{AJAX_BASE_URL}/user/{TEST_USER_ID}"
    mock_error_response_body = {
        "error": True,
        "message": "Full info not available",
        "body": {"some": "data"},
    }
    respx.get(mock_url, params={"full": "1"}).mock(
        return_value=Response(200, json=mock_error_response_body)
    )

    result = web_api.get_user_info_full(TEST_USER_ID)

    assert isinstance(result, WebAjaxApiError)
    assert result.error is True
    assert result.message == "Full info not available"
    assert result.body == {"some": "data"}


# --- Tests for get_user_profile_all ---

# Example response for profile/all, obtained earlier
EXAMPLE_USER_PROFILE_ALL_RESPONSE = {
  "error": False,
  "message": "",
  "body": {
    "illusts": {
      "97164570": None, "96581228": None, "95989414": None, "95747170": None,
      "95302044": None, "95065717": None, "94867922": None, "93583940": None,
      "91428641": None, "90646050": None, "90217294": None, "89658468": None,
      "89502354": None, "86968678": None, "84708129": None, "84278335": None,
      "80781665": None, "79963938": None, "79448157": None, "79415116": None,
      "78524726": None, "70448486": None, "69504408": None, "63237917": None,
      "58658636": None, "44196672": None, "44080057": None, "43939060": None,
      "43552613": None
    },
    "manga": {"94691329": None},
    "novels": [],
    "mangaSeries": [
      {"id": "139494", "userId": "9153585", "title": "ナツメと性愛対決", "description": "", "caption": "", "total": 5, "content_order": None, "url": None, "coverImageSl": None, "firstIllustId": "94691329", "latestIllustId": "98595210", "createDate": "2021-12-10T21:56:59+09:00", "updateDate": "2022-05-25T19:00:08+09:00", "watchCount": None, "isWatched": False, "isNotifying": False},
      {"id": "137061", "userId": "9153585", "title": "ナツメ１７", "description": "", "caption": "", "total": 4, "content_order": None, "url": None, "coverImageSl": None, "firstIllustId": "93990820", "latestIllustId": "93921150", "createDate": "2021-11-17T22:37:16+09:00", "updateDate": "2021-11-17T23:38:52+09:00", "watchCount": None, "isWatched": False, "isNotifying": False}
    ],
    "novelSeries": [],
    "pickup": [
      {"type": "fanbox", "deletable": False, "draggable": True, "userName": "haku89", "userImageUrl": "https://i.pximg.net/user-profile/img/2018/06/26/14/26/03/14408330_3de67ff59732d611d71369bddd8ea287_170.jpg", "contentUrl": "https://www.pixiv.net/fanbox/creator/9153585?utm_campaign=www_profile&utm_medium=site_flow&utm_source=pixiv", "description": "コメントや評価ありがとうございます！\\r\\nhakuです。よろしく！\\r\\n日本語おk、簡単な英語おk\\r\\n\\r\\n興味で絵を描いて生きています、", "imageUrl": "https://pixiv.pximg.net/c/520x280_90_a2_g5/fanbox/public/images/creator/9153585/cover/6zdB1tF7f5YUQqLDfsTr9mpL.jpeg", "imageUrlMobile": "https://pixiv.pximg.net/c/520x280_90_a2_g5/fanbox/public/images/creator/9153585/cover/6zdB1tF7f5YUQqLDfsTr9mpL.jpeg", "hasAdultContent": True},
      {"id": "79448157", "title": "端木鱼", "illustType": 0, "xRestrict": 0, "restrict": 0, "sl": 2, "url": "https://i.pximg.net/c/288x288_80_a2/img-master/img/2020/08/12/13/22/12/79448157_p0_square1200.jpg", "description": "", "tags": ["可愛い", "女の子", "花嫁", "白髪", "風景", "かわいらしい", "ふつくしい", "クリック推薦", "端木鱼", "オリジナル1000users入り"], "userId": "9153585", "userName": "haku89", "width": 4299, "height": 2643, "pageCount": 1, "isBookmarkable": True, "bookmarkData": None, "alt": "#可愛い 端木鱼 - haku89のイラスト", "titleCaptionTranslation": {"workTitle": None, "workCaption": None}, "createDate": "2020-02-13T00:24:22+09:00", "updateDate": "2020-08-12T13:22:12+09:00", "isUnlisted": False, "isMasked": False, "urls": {"250x250": "https://i.pximg.net/c/250x250_80_a2/img-master/img/2020/08/12/13/22/12/79448157_p0_square1200.jpg", "360x360": "https://i.pximg.net/c/360x360_70/img-master/img/2020/08/12/13/22/12/79448157_p0_square1200.jpg", "540x540": "https://i.pximg.net/c/540x540_70/img-master/img/2020/08/12/13/22/12/79448157_p0_square1200.jpg"}, "type": "illust", "deletable": True, "draggable": True, "contentUrl": "https://www.pixiv.net/artworks/79448157"}
    ],
    "bookmarkCount": {"public": {"illust": 1, "novel": 0}, "private": {"illust": 0, "novel": 0}},
    "externalSiteWorksStatus": {"booth": True, "sketch": True, "vroidHub": True},
    "request": {"showRequestTab": False, "showRequestSentTab": False, "postWorks": {"artworks": [], "novels": []}}
  }
}

@respx.mock
def test_get_user_profile_all_success(web_api: WebPixivAPI):
    """Test successful retrieval of user profile/all (sync)."""
    mock_url = f"{AJAX_BASE_URL}/user/{TEST_USER_ID}/profile/all"
    respx.get(mock_url).mock(
        return_value=Response(200, json=EXAMPLE_USER_PROFILE_ALL_RESPONSE)
    )

    result = web_api.get_user_profile_all(TEST_USER_ID)

    assert isinstance(result, WebUserProfileAllBody)
    assert result.illusts is not None
    assert "97164570" in result.illusts
    assert result.manga_series is not None
    assert len(result.manga_series) == 2
    assert result.manga_series[0].title == "ナツメと性愛対決"
    assert result.pickup is not None
    assert len(result.pickup) == 2
    assert result.pickup[0].type == "fanbox"
    assert result.pickup[1].type == "illust"
    assert result.bookmark_count is not None
    assert result.bookmark_count.public.illust == 1


@pytest.mark.asyncio
@respx.mock
async def test_async_get_user_profile_all_success(web_api: WebPixivAPI):
    """Test successful retrieval of user profile/all (async)."""
    mock_url = f"{AJAX_BASE_URL}/user/{TEST_USER_ID}/profile/all"
    respx.get(mock_url).mock(
        return_value=Response(200, json=EXAMPLE_USER_PROFILE_ALL_RESPONSE)
    )

    result = await web_api.async_get_user_profile_all(TEST_USER_ID)

    assert isinstance(result, WebUserProfileAllBody)
    assert result.illusts is not None
    assert "97164570" in result.illusts
    assert result.manga_series is not None
    assert len(result.manga_series) == 2


# --- Tests for get_user_following ---

# Example response for the following endpoint
EXAMPLE_USER_FOLLOWING_RESPONSE = {
  "error": False,
  "message": "",
  "body": {
    "users": [
      {"userId": "5083537", "userName": "RAI", "profileImageUrl": "https://i.pximg.net/user-profile/img/2020/04/03/10/29/02/18251768_c26449c8f7bfe4cbb2c345ae3d7ea0f3_170.jpg", "userComment": "...", "following": False, "followed": False, "isBlocking": False, "isMypixiv": False, "illusts": [{"id": "101010718", "title": "ウタゲ", "illustType": 0, "xRestrict": 0, "restrict": 0, "sl": 2, "url": "https://i.pximg.net/c/250x250_80_a2/img-master/img/2022/09/05/08/46/48/101010718_p0_square1200.jpg", "description": "", "tags": ["ウタゲ", "Arknights", "アークナイツ", "明日方舟", "rkgk"], "userId": "5083537", "userName": "RAI", "width": 694, "height": 1284, "pageCount": 1, "isBookmarkable": True, "bookmarkData": None, "alt": "#ウタゲ ウタゲ - RAIのイラスト", "titleCaptionTranslation": {"workTitle": None, "workCaption": None}, "createDate": "2022-09-05T08:46:48+09:00", "updateDate": "2022-09-05T08:46:48+09:00", "isUnlisted": False, "isMasked": False, "profileImageUrl": "https://i.pximg.net/user-profile/img/2020/04/03/10/29/02/18251768_c26449c8f7bfe4cbb2c345ae3d7ea0f3_50.jpg"}], "novels": [], "acceptRequest": False},
      {"userId": "61362279", "userName": "老陳LaoChen🔥", "profileImageUrl": "...", "userComment": "...", "following": False, "followed": False, "isBlocking": False, "isMypixiv": False, "illusts": [{"id": "100903553", "title": "jk大凤r18差分", "illustType": 0, "xRestrict": 1, "restrict": 0, "sl": 6, "url": "...", "description": "", "tags": ["R-18", "巨乳", "大鳳(アズールレーン)", "アズールレーン", "タイツ足裏", "タイツ", "下校後の甘い時間", "くぱぁ", "アズールレーン500users入り", "風紀を乱す風紀委員"], "userId": "61362279", "userName": "老陳LaoChen🔥", "width": 1152, "height": 1920, "pageCount": 4, "isBookmarkable": True, "bookmarkData": None, "alt": "...", "titleCaptionTranslation": {"workTitle": None, "workCaption": None}, "createDate": "2022-08-31T22:59:35+09:00", "updateDate": "2022-08-31T22:59:35+09:00", "isUnlisted": False, "isMasked": False, "profileImageUrl": "..."}], "novels": [], "acceptRequest": False},
      {"userId": "1680108", "userName": "ふむゆん", "profileImageUrl": "...", "userComment": "...", "following": False, "followed": False, "isBlocking": False, "isMypixiv": False, "illusts": [{"id": "100307516", "title": "C100", "illustType": 0, "xRestrict": 0, "restrict": 0, "sl": 2, "url": "...", "description": "", "tags": ["オリジナル", "オフショルダーワンピース", "ドレス", "女の子", "黒髪", "オリジナル3000users入り"], "userId": "1680108", "userName": "ふむゆん", "width": 1556, "height": 2593, "pageCount": 1, "isBookmarkable": True, "bookmarkData": None, "alt": "...", "titleCaptionTranslation": {"workTitle": None, "workCaption": None}, "createDate": "2022-08-07T20:45:36+09:00", "updateDate": "2022-08-07T20:46:06+09:00", "isUnlisted": False, "isMasked": False, "profileImageUrl": "..."}], "novels": [], "acceptRequest": False}
      # Truncated for brevity
    ],
    "total": 353,
    # Skipping followUserTags, zoneConfig, extraData for brevity
  }
}

@respx.mock
def test_get_user_following_success(authenticated_web_api: WebPixivAPI):
    """Test successful retrieval of following users (sync)."""
    mock_url = f"{AJAX_BASE_URL}/user/{TEST_USER_ID}/following"
    params = {"offset": "0", "limit": "3", "rest": "show"}
    respx.get(mock_url, params=params).mock(
        return_value=Response(200, json=EXAMPLE_USER_FOLLOWING_RESPONSE)
    )

    result = authenticated_web_api.get_user_following(TEST_USER_ID, offset=0, limit=3)

    assert isinstance(result, WebFollowingUserBody)
    assert result.total == 353
    assert len(result.users) == 3
    assert result.users[0].user_id == 5083537
    assert result.users[0].user_name == "RAI"
    assert len(result.users[0].illusts) > 0
    assert result.users[0].illusts[0].title == "ウタゲ"


@pytest.mark.asyncio
@respx.mock
async def test_async_get_user_following_success(authenticated_web_api: WebPixivAPI):
    """Test successful retrieval of following users (async)."""
    mock_url = f"{AJAX_BASE_URL}/user/{TEST_USER_ID}/following"
    params = {"offset": "0", "limit": "3", "rest": "show"}
    respx.get(mock_url, params=params).mock(
        return_value=Response(200, json=EXAMPLE_USER_FOLLOWING_RESPONSE)
    )

    result = await authenticated_web_api.async_get_user_following(TEST_USER_ID, offset=0, limit=3)

    assert isinstance(result, WebFollowingUserBody)
    assert result.total == 353
    assert len(result.users) == 3


@respx.mock
def test_get_user_following_requires_auth(web_api: WebPixivAPI):
    """Test that get_user_following raises error if not authenticated."""
    with pytest.raises(PixivError, match="Authentication required"):
        web_api.get_user_following(TEST_USER_ID, offset=0, limit=3)


# TODO: Add tests for authenticated endpoints when implemented, like POST requests
# def test_some_authenticated_endpoint(authenticated_web_api: WebPixivAPI):
#     ...
