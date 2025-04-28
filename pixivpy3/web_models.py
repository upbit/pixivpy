import datetime
from typing import Any, Generic, List, Optional, TypeVar, Union, Annotated

import pydantic

from pydantic import BaseModel, AfterValidator, AliasChoices
from pydantic.functional_validators import AfterValidator, BeforeValidator

# Import Base Model and config handling based on Pydantic version
if pydantic.__version__.startswith("1."):
    from pydantic import BaseModel, Field

    def _to_pascal(string: str) -> str:
        return "".join(word.capitalize() for word in string.split("_"))

    def _to_camel(string: str) -> str:
        if len(string) >= 1:
            pascal_string = _to_pascal(string)
            return pascal_string[0].lower() + pascal_string[1:]
        return string.lower()

    to_camel = _to_camel
    ConfigDict = dict
else:
    # Assume Pydantic v2+
    from pydantic import BaseModel, ConfigDict, Field # type: ignore[assignment]
    from pydantic.alias_generators import to_camel # type: ignore[assignment]



def convert_dict_to_intlist(v: Any) -> list[int]:
    if isinstance(v, dict):
        return [int(key) for key in v.keys()]
    elif isinstance(v, list):
        return [int(item) for item in v]
    raise ValueError("Input must be a dict or list")

# 定义可复用的类型别名
DictKeysAsIntList = Annotated[
    list[int],  # 静态类型和运行时类型
    BeforeValidator(convert_dict_to_intlist)  # 转换逻辑
]

class BaseWebModel(BaseModel):
    """Base model for Web Ajax API responses with camelCase alias handling."""
    if pydantic.__version__.startswith("2."):
        model_config = ConfigDict(
            extra="allow", # Allow unexpected fields from API
            populate_by_name=True,
            alias_generator=to_camel,
        )
    else: # Pydantic v1
        class Config:
            extra = "allow"
            alias_generator = to_camel
            allow_population_by_field_name = True # Allow using both snake_case and camelCase

    if pydantic.__version__.startswith("1."):
         # Add model_validate for Pydantic v1 compatibility
        @classmethod
        def model_validate(cls, obj: Any) -> "BaseWebModel": # type: ignore[override]
             # Note: Use Self in Python 3.11+
            return cls.parse_obj(obj)

    def __getitem__(self, item: str) -> Any:
        # Allow accessing fields using `[]` for backward compatibility
        return getattr(self, item)

# Type variable for the 'body' of the Ajax response
BodyT = TypeVar("BodyT")


class WebAjaxApiError(BaseWebModel):
    """Represents a structured error returned by the Pixiv Web Ajax API."""
    error: bool = True # Should always be true for this model
    message: str
    body: Any # Include the original body for inspection if needed


class BaseAjaxResponse(BaseWebModel, Generic[BodyT]):
    """Generic base model for the standard Pixiv Ajax JSON response structure."""
    error: bool
    message: str
    body: BodyT

class WebNovelBookmarkData(BaseWebModel):
    id: int
    private: bool


# --- Models for /ajax/user/{USER_ID} ---

class WebUserInfoShort(BaseWebModel):
    """Model for the short user info returned by /ajax/user/{USER_ID}."""
    user_id: int
    name: str
    image: str # URL for 50px avatar
    image_big: str # URL for 170px avatar
    premium: bool
    is_followed: bool
    is_mypixiv: bool # Friend status
    is_blocking: bool # Whether the requesting user is blocking this user
    background: Optional[Any] # Usually null? Structure unknown
    sketch_live_id: Optional[str] = None # Active Pixiv Sketch live stream ID?
    partial: int # Meaning unknown, seems to be 0
    accept_request: Optional[bool] = None # Whether the user accepts requests
    sketch_lives: List[Any] # Seems to be always empty in examples




# --- Models for /ajax/user/{USER_ID}?full=1 ---

class WebUserSocialTwitter(BaseWebModel):
    url: str

class WebUserSocial(BaseWebModel):
    twitter: Optional[WebUserSocialTwitter] = None
    # Add other social platforms here if they appear in responses

class WebUserRegion(BaseWebModel):
    name: Optional[str]
    region: Optional[str] # Country code? e.g., "JP"
    prefecture: Optional[str] # Prefecture ID?
    privacy_level: Optional[int] # Typically "0"

class WebUserAge(BaseWebModel):
    name: Optional[str] # e.g., "23歳"
    privacy_level: Optional[int]

class WebUserBirthDay(BaseWebModel):
    name: Optional[str] # e.g., "12月16日"
    privacy_level: Optional[int]

class WebUserGender(BaseWebModel):
    name: Optional[str] # e.g., "女性"
    privacy_level: Optional[int]

class WebUserJob(BaseWebModel):
    name: Optional[str]
    privacy_level: Optional[int]

class WebUserWorkspace(BaseWebModel):
    pc: Optional[str] = Field(default=None, alias='userWorkspacePc')
    monitor: Optional[str] = Field(default=None, alias='userWorkspaceMonitor')
    tool: Optional[str] = Field(default=None, alias='userWorkspaceTool')
    scanner: Optional[str] = Field(default=None, alias='userWorkspaceScanner')
    tablet: Optional[str] = Field(default=None, alias='userWorkspaceTablet')
    mouse: Optional[str] = Field(default=None, alias='userWorkspaceMouse')
    printer: Optional[str] = Field(default=None, alias='userWorkspacePrinter')
    desktop: Optional[str] = Field(default=None, alias='userWorkspaceDesktop')
    music: Optional[str] = Field(default=None, alias='userWorkspaceMusic')
    desk: Optional[str] = Field(default=None, alias='userWorkspaceDesk')
    chair: Optional[str] = Field(default=None, alias='userWorkspaceChair')
    comment: Optional[str] = Field(default=None, alias='userWorkspaceComment')
    workspace_image_url: Optional[str] = Field(default=None, alias='userWorkspaceImageUrl')

class WebUserGroup(BaseWebModel):
    id: int
    title: str
    icon_url: str


class WebUserInfoFull(WebUserInfoShort): # Inherits fields from short version
    """Model for the full user info returned by /ajax/user/{USER_ID}?full=1."""
    # Fields also present in WebUserInfoShort:
    # userId, name, image, imageBig, premium, isFollowed, isMypixiv, isBlocking,
    # background, sketchLiveId, partial, acceptRequest, sketchLives

    # Additional fields in 'full' response:
    following: int # Number of users followed
    followed_back: bool
    comment: Optional[str] = None # User profile comment (plain text)
    comment_html: Optional[str] = None # User profile comment (HTML)
    webpage: Optional[str] = None
    social: Any # List of social media links
    can_send_message: bool # Whether the requesting user can send message
    region: WebUserRegion
    age: WebUserAge
    birth_day: WebUserBirthDay
    gender: WebUserGender
    job: WebUserJob
    workspace: Optional[WebUserWorkspace] = None
    official: bool # Is this an official Pixiv account?
    group: Optional[List[WebUserGroup]] = None # List of groups the user belongs to





# --- Models for /ajax/user/{USER_ID}/profile/all ---

class WebMangaSeries(BaseWebModel):
    id: int
    user_id: int
    title: str
    description: str
    caption: str
    total: int
    content_order: Optional[Any] = None # Type unclear from example
    url: Optional[str] = None # Always null in example?
    cover_image_sl: Optional[int] = None # Sanity level?
    first_illust_id: int
    latest_illust_id: int
    create_date: datetime.datetime # ISO 8601 format with timezone
    update_date: datetime.datetime # ISO 8601 format with timezone
    watch_count: Optional[int] = None # Always null?
    is_watched: bool
    is_notifying: bool


class WebPickupFanbox(BaseWebModel):
    type: str # "fanbox"
    deletable: bool
    draggable: bool
    user_name: str
    user_image_url: str
    content_url: str # URL to fanbox page
    description: str
    image_url: str # Cover image URL
    image_url_mobile: str # Mobile cover image URL
    has_adult_content: bool


class WebPickupUrls(BaseWebModel):
    # Aliases handled by BaseWebModel config
    url_250x250: str = Field(alias="250x250")
    url_360x360: str = Field(alias="360x360")
    url_540x540: str = Field(alias="540x540")

class WebCoverUrls(BaseWebModel):
    url_240mw: Optional[str] = Field(default=None, alias="240mw")
    url_480mw: Optional[str] = Field(default=None, alias="480mw")
    url_1200x1200: Optional[str] = Field(default=None, alias="1200x1200")
    url_128x128: Optional[str] = Field(default=None, alias="128x128")
    url_original: Optional[str] = Field(default=None, alias="original")

class WebPickupIllust(BaseWebModel):
    id: int
    title: str
    illust_type: int # 0 for illust, 1 for manga?
    x_restrict: int
    restrict: int
    sl: int # Scaling level?
    url: str # Thumbnail URL? Matches urls['250x250'] base
    description: str
    tags: List[str]
    user_id: int
    user_name: str
    width: int
    height: int
    page_count: int
    is_bookmarkable: bool
    bookmark_data: Optional[Any] = None # Structure unknown
    alt: str
    # titleCaptionTranslation: Optional[Any] = None # Structure unknown
    create_date: datetime.datetime # ISO 8601 format with timezone
    update_date: datetime.datetime # ISO 8601 format with timezone
    is_unlisted: bool
    is_masked: bool
    # urls: WebPickupUrls
    type: str # "illust"
    deletable: bool
    draggable: bool
    content_url: str # URL to artwork page


class WebNovelInfoBase(BaseWebModel):
    ai_type: int
    bookmark_count: Optional[int] = None
    bookmark_data: Optional[WebNovelBookmarkData] = None
    create_date: datetime.datetime
    description: str
    genre: int
    id: int
    is_bookmarkable: bool
    is_masked: bool
    is_original: bool
    is_unlisted: bool
    marker: Optional[Any] = None
    profile_image_url: str
    reading_time: int
    restrict: int
    tags: List[str]
    text_count: int = Field(validation_alias=AliasChoices("textCount", "characterCount"))
    title: str
    title_caption_translation: Optional[dict[str, Optional[str]]] = None
    update_date: datetime.datetime = Field(validation_alias=AliasChoices("updateDate", "uploadDate"))
    cover_url: str = Field(validation_alias=AliasChoices("url", "coverUrl"))# Novel cover image URL
    use_word_count: bool
    user_id: int
    user_name: str
    visibility_scope: int
    word_count: int
    x_restrict: int
    extra_data: Any = Field(default=None, exclude=True) # Exclude from model validation
    zone_config: Any = Field(default=None, exclude=True) # Exclude from model validation

# --- 为新的 tags 结构定义辅助模型 ---
class TagItem(BaseWebModel):
    tag: str
    locked: bool
    deletable: bool
    user_id: int
    user_name: str

class TagsInfo(BaseWebModel):
    author_id: int
    is_locked: bool
    tags: List[TagItem]
    writable: bool

class WebPickupNovel(WebNovelInfoBase):
    type: str = 'novel'
    draggable: bool
    content_url: str
    deletable: bool

class WebListedUserNovel(WebNovelInfoBase):
    series_id: Optional[int] = None
    series_title: Optional[str] = None

# --- 定义继承的 WebNovelInfoFull 类 ---
class WebNovelInfoFull(WebNovelInfoBase):
    # --- 字段覆盖 ---
    tags: TagsInfo # 覆盖基类的 List[str] 类型

    # --- 从 JSON 添加的新字段 (不在 Base 中, 且不是 extraData) ---
    comment_count: int
    marker_count: int
    like_count: int
    page_count: int
    view_count: int
    is_bungei: bool
    content: str
    suggested_settings: Optional[dict[str, Any]] = None
    like_data: bool
    poll_data: Optional[Any] = None
    series_nav_data: Optional[Any] = None
    description_booth_id: Optional[str] = None
    description_youtube_id: Optional[str] = None
    comic_promotion: Optional[Any] = None
    fanbox_promotion: Optional[Any] = None
    contest_banners: List[Any] = Field(default_factory=list)
    contest_data: Optional[Any] = None # 对应 contestData
    # request: Optional[Any] = None # 对应 request, 如果需要的话取消注释
    image_response_out_data: List[Any] = Field(default_factory=list)
    image_response_data: List[Any] = Field(default_factory=list)
    image_response_count: int
    user_novels: dict[int, Optional[WebListedUserNovel]]
    has_glossary: bool
    language: str
    text_embedded_images: Optional[Any] = None
    comment_off: int
    is_login_only: bool
    is_masked:None = Field(default=None, exclude=True)
    visibility_scope:None = Field(default=None, exclude=True)
    profile_image_url:None = Field(default=None, exclude=True)






class WebNovelSeries(BaseWebModel):
    ai_type: int
    caption: str
    cover: dict[str, dict[str, str]]
    cover_setting_data: Optional[Any] = None
    create_date: datetime.datetime
    created_timestamp: int
    display_series_content_count: int
    first_episode: dict[str, str]
    first_novel_id: int
    genre_id: int
    id: int
    is_concluded: bool
    is_notifying: bool
    is_original: bool
    is_watched: bool
    language: str
    last_published_content_timestamp: int
    latest_novel_id: int
    max_x_restrict: Optional[Any] = None
    profile_image_url: str
    published_content_count: int
    published_reading_time: int
    published_total_character_count: int
    published_total_word_count: int
    share_text: str
    tags: List[str]
    title: str
    total: int
    update_date: datetime.datetime
    updated_timestamp: int
    use_word_count: bool
    user_id: int
    user_name: str
    watch_count: Optional[Any] = None
    x_restrict: int


class WebNovelSeriesInfo(WebNovelSeries):
    has_glossary: bool



class WebBookmarkCountDetail(BaseWebModel):
    illust: int
    novel: int

class WebBookmarkCount(BaseWebModel):
    public: WebBookmarkCountDetail
    private: WebBookmarkCountDetail


class WebExternalSiteWorksStatus(BaseWebModel):
    booth: bool
    sketch: bool
    vroid_hub: bool = Field(alias="vroidHub")


class WebRequestPostWorks(BaseWebModel):
    artworks: List[Any] # Structure unknown
    novels: List[Any] # Structure unknown

class WebRequestInfo(BaseWebModel):
    show_request_tab: bool
    show_request_sent_tab: bool
    post_works: WebRequestPostWorks


class WebUserProfileAll(BaseWebModel):
    illusts: DictKeysAsIntList # Keys are illust IDs, values are null?
    manga: DictKeysAsIntList # Keys are manga IDs, values are null?
    novels: DictKeysAsIntList # Keys are novel IDs, values are null?
    manga_series: List[WebMangaSeries]
    novel_series: List[WebNovelSeries]
    # Pickup can contain Fanbox info or Illust info
    pickup: Optional[List[Union[WebPickupFanbox, WebPickupIllust, WebPickupNovel]]] = None
    bookmark_count: Optional[WebBookmarkCount] = None
    external_site_works_status: Optional[WebExternalSiteWorksStatus] = None
    request: Optional[WebRequestInfo] = None





# --- Models for /ajax/user/{USER_ID}/following ---

class WebListedUserIllust(BaseWebModel):
    """Model for illustrations embedded within the following user list."""
    id: int
    title: str
    illust_type: int
    x_restrict: int
    restrict: int
    sl: int
    ai_type: int
    url: str # Thumbnail URL
    description: str
    tags: List[str]
    user_id: int
    user_name: str
    width: int
    height: int
    page_count: int
    is_bookmarkable: bool
    bookmark_data: Optional[Any] = None
    alt: str
    titleCaptionTranslation: Optional[Any] = None # Simplified, assuming structure is similar
    create_date: datetime.datetime
    update_date: datetime.datetime
    is_unlisted: bool
    is_masked: bool
    visibility_scope: int # tried to figure out...
    profile_image_url: str


class WebUserCommision(BaseWebModel):
    accept_request: bool
    isSubscribedReopenNotification: bool

class WebListedUserInfo(BaseWebModel):
    """Model for a single user in the following list."""
    user_id: int
    user_name: str
    profile_image_url: str
    user_comment: str
    following: bool # Should always be True?
    followed: bool # Alias for followed_back?
    is_blocking: bool
    is_mypixiv: bool
    illusts: List[WebListedUserIllust]
    novels: List[WebListedUserNovel] # Assuming empty based on example
    commission: Optional[WebUserCommision]

class WebListedUser(BaseWebModel):
    users: List[WebListedUserInfo]
    total: int

class WebFollowingUser(WebListedUser):
    follow_user_tags: list[Any]

class WebFollowersUser(WebListedUser):
    pass






# --- Models for /ajax/user/{USER_ID}/followers ---
# The structure is very similar to the /following endpoint,
# so we reuse WebFollowingUserBody



# --- Models for /ajax/user/{USER_ID}/works/latest ---

# Reuse WebFollowingUserIllust as the structure seems identical
# for illustration details in this endpoint.

class WebUserLatestWorks(BaseWebModel):
    """Model for the body of the user latest works response."""
    # Keys are illust IDs (str). Values can be illust details or null.
    illusts: Optional[dict[str, Optional[WebListedUserIllust]]] = None
    novels: Optional[List[Any]] = None # Structure unknown, empty in example
