from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class BasePixivpyModel(BaseModel):
    # Note for `extra`:
    # until some version, `pydantic` does not show extra fields on `str` / `repr`
    model_config = ConfigDict(
        extra="allow",  # set `forbid` to detect extra fields and update models
    )


# Instead of returning `null`, Pixiv return `{}` for empty objects
# Have this class to handle such cases and don't make nullable fields
class EmptyObject(BasePixivpyModel):
    # By default, `pydantic` always returns `True` for `__bool__` method
    def __bool__(self) -> bool:
        return False


class ProfileImageUrls(BasePixivpyModel):
    medium: str


class UserInfo(BasePixivpyModel):
    id: int
    name: str
    account: str
    profile_image_urls: ProfileImageUrls
    comment: Optional[str] = None  # present only on `user_detail` endpoint
    is_followed: Optional[bool]
    is_access_blocking_user: Optional[bool] = None


class CommentUser(BasePixivpyModel):
    id: int
    name: str
    account: str
    profile_image_urls: ProfileImageUrls


class Profile(BasePixivpyModel):
    webpage: Optional[str]
    gender: str
    birth: str
    birth_day: str
    birth_year: int
    region: str
    address_id: int
    country_code: str
    job: str
    job_id: int
    total_follow_users: int
    total_mypixiv_users: int
    total_illusts: int
    total_manga: int
    total_novels: int
    total_illust_bookmarks_public: int
    total_illust_series: int
    total_novel_series: int
    background_image_url: str
    twitter_account: str
    twitter_url: Optional[str]
    pawoo_url: Optional[str]
    is_premium: bool
    is_using_custom_profile_image: bool


class ProfilePublicity(BasePixivpyModel):
    gender: str
    region: str
    birth_day: str
    birth_year: str
    job: str
    pawoo: bool


class Workspace(BasePixivpyModel):
    pc: str
    monitor: str
    tool: str
    scanner: str
    tablet: str
    mouse: str
    printer: str
    desktop: str
    music: str
    desk: str
    chair: str
    comment: str
    workspace_image_url: Optional[str]


class UserInfoFull(BasePixivpyModel):
    user: UserInfo
    profile: Profile
    profile_publicity: ProfilePublicity
    workspace: Workspace


class ImageUrls(BasePixivpyModel):
    square_medium: str
    medium: str
    large: str


class NovelTag(BasePixivpyModel):
    name: str
    translated_name: Optional[str]
    added_by_uploaded_user: bool


class IllustrationTag(BasePixivpyModel):
    name: str
    translated_name: Optional[str]


class Series(BasePixivpyModel):
    id: int
    title: str


class NovelInfo(BasePixivpyModel):
    id: int
    title: str
    caption: str
    restrict: int
    x_restrict: int
    is_original: bool
    image_urls: ImageUrls
    create_date: str
    tags: List[NovelTag]
    page_count: int
    text_length: int
    user: UserInfo
    series: Union[Series, EmptyObject]
    is_bookmarked: bool
    total_bookmarks: int
    total_view: int
    visible: bool
    total_comments: int
    is_muted: bool
    is_mypixiv_only: bool
    is_x_restricted: bool
    novel_ai_type: int
    comment_access_control: Optional[int] = None


class Comment(BasePixivpyModel):
    id: int
    comment: str
    date: str
    user: Optional[CommentUser]
    parent_comment: Union["Comment", EmptyObject]


class NovelComments(BasePixivpyModel):
    total_comments: int
    comments: List[Comment]
    next_url: Optional[str]
    comment_access_control: int


class NovelNavigationInfo(BasePixivpyModel):
    id: int
    viewable: bool
    content_order: str
    title: str
    cover_url: str
    viewable_message: Optional[str]


class WebviewNovel(BasePixivpyModel):
    # This model is extracted from `HTML`, so it has `camelCase` fields
    # For more details, see: https://github.com/upbit/pixivpy/issues/337
    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="allow",  # see `novel_text` method for reasons
    )

    id: str
    title: str
    series_id: Optional[str]
    series_title: Optional[str]
    series_is_watched: Optional[bool]
    user_id: str
    cover_url: str
    tags: List[str]
    caption: str
    cdate: str
    rating: Dict[str, int]
    text: str
    marker: Optional[str]
    illusts: List[str]
    images: List[str]
    series_navigation: Optional[NovelNavigationInfo]
    glossary_items: List[str]
    replaceable_item_ids: List[str]
    ai_type: int
    is_original: bool


class UserBookmarksNovel(BasePixivpyModel):
    novels: List[NovelInfo]
    next_url: Optional[str]


class UserNovels(BasePixivpyModel):
    user: UserInfo
    novels: List[NovelInfo]
    next_url: Optional[str]


class SearchNovel(BasePixivpyModel):
    novels: List[NovelInfo]
    next_url: Optional[str]
    search_span_limit: int
    show_ai: bool


class MetaSinglePage(BasePixivpyModel):
    original_image_url: Optional[str] = None


class MetaPage(BasePixivpyModel):
    image_urls: Dict[str, str]


class IllustrationInfo(BasePixivpyModel):
    id: int
    title: str
    type: str
    image_urls: ImageUrls
    caption: str
    restrict: int
    user: UserInfo
    tags: List[IllustrationTag]
    tools: List[str]
    create_date: str
    page_count: int
    width: int
    height: int
    sanity_level: int
    x_restrict: int
    series: Any
    meta_single_page: MetaSinglePage
    meta_pages: List[MetaPage]
    total_view: int
    total_bookmarks: int
    is_bookmarked: bool
    visible: bool
    is_muted: bool
    illust_ai_type: int
    illust_book_style: int
    total_comments: Optional[int] = None
    restriction_attributes: List[str] = Field(default_factory=list)


class SearchIllustrations(BasePixivpyModel):
    illusts: List[IllustrationInfo]
    next_url: Optional[str]
    search_span_limit: int
    show_ai: bool


class UserBookmarksIllustrations(BasePixivpyModel):
    illusts: List[IllustrationInfo]
    next_url: Optional[str]


class UserPreview(BasePixivpyModel):
    user: UserInfo
    illusts: List[IllustrationInfo]
    novels: List[NovelInfo]
    is_muted: bool


class UserFollowing(BasePixivpyModel):
    user_previews: List[UserPreview]
    next_url: Optional[str]


class UserIllustrations(BasePixivpyModel):
    user: UserInfo
    illusts: List[IllustrationInfo]
    next_url: Optional[str]
