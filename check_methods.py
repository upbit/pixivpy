"""
File to check all methods of the Pixiv API.
When some new ids are found, that break models in code, add them here.
Also add the reason why a new id is added (e.g., breaks `Model.some_field`).

Advise:
- If you want to check for any new fields sent by Pixiv,
  set `BasePixivpyModel.model_config.extra` to `forbid`;
"""

import os

from pixivpy3 import AppPixivAPI

# Simply override this in code for personal use
# But keep it environment variable as more general approach
ACCESS_TOKEN = os.environ["PIXIV_ACCESS_TOKEN"]
REFRESH_TOKEN = os.environ["PIXIV_REFRESH_TOKEN"]

client = AppPixivAPI()
client.set_auth(access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

# Test variables
USER_IDS = [
    1226647,  # R18, Illustrations, Manga, Ugoria, Bookmarks
    18250910,  # Novels
]
ILLUSTRATION_IDS = [
    126076729,  # Ugoria, R18
    125723831,  # Illustration
    125478796,  # Manga
]
NOVEL_IDS = [
    23778687,  # R18
    23722335,  # Has empty object for `seriesNavigation`
    22133267,  # Has `none` for `seriesNavigation`
]
SEARCH_WORDS = [
    "asuka",
    "R-18",
    "コードギアス",
]
UGORIA_IDS = [
    126076729,  # R18
    120938552,  # all-ages
]
NOVEL_SERIES_IDS = [
    12863221,
]
SHOWCASE_ARTICLE_IDS = []  # I don't know how to get these

# Some random illustration to add and remove from bookmarks
BOOKMARKS_ILLUSTRATION_ID = 126201642
# Some random user to follow and unfollow
BOOKMARKS_USER_ID = 41895485
# Whether to enable AI show settings
ENABLE_AI_SHOW_SETTINGS = "true"  # Literal["true", "false"]

# models
for user_id in USER_IDS:
    user_detail_res = client.user_detail(user_id=user_id)
    print("user_detail", user_detail_res)

# models
for user_id in USER_IDS:
    user_illusts_res = client.user_illusts(user_id=user_id)
    print("user_illusts", user_illusts_res)

# models
for user_id in USER_IDS:
    user_bookmarks_illust_res = client.user_bookmarks_illust(user_id=user_id)
    print("user_bookmarks_illust", user_bookmarks_illust_res)

# models
for user_id in USER_IDS:
    user_bookmarks_novel_res = client.user_bookmarks_novel(user_id=user_id)
    print("user_bookmarks_novel", user_bookmarks_novel_res)

# no models
for user_id in USER_IDS:
    user_related_res = client.user_related(seed_user_id=user_id)
    print("user_related", user_related_res)

# no models
user_recommended_res = client.user_recommended()
print("user_recommended", user_recommended_res)

# no models
illust_follow_res = client.illust_follow()
print("illust_follow", illust_follow_res)

# no models
for illustration_id in ILLUSTRATION_IDS:
    illust_detail_res = client.illust_detail(illust_id=illustration_id)
    print("illust_detail", illust_detail_res)

# no models
for illustration_id in ILLUSTRATION_IDS:
    illust_comments_res = client.illust_comments(illust_id=illustration_id)
    print("illust_comments", illust_comments_res)

# no models
for illustration_id in ILLUSTRATION_IDS:
    illust_related_res = client.illust_related(illust_id=illustration_id)
    print("illust_related", illust_related_res)

# no models
illust_recommended_res = client.illust_recommended()
print("illust_recommended", illust_recommended_res)

# models
for novel_id in NOVEL_IDS:
    novel_comments_res = client.novel_comments(novel_id=novel_id)
    print("novel_comments", novel_comments_res)

# no models
novel_recommended_res = client.novel_recommended()
print("novel_recommended", novel_recommended_res)

# no models
illust_ranking_res = client.illust_ranking()
print("illust_ranking", illust_ranking_res)

# no models
trending_tags_illust_res = client.trending_tags_illust()
print("trending_tags_illust", trending_tags_illust_res)

# models
for search_word in SEARCH_WORDS:
    search_illust_res = client.search_illust(word=search_word)
    print("search_illust", search_illust_res)

# models
for search_word in SEARCH_WORDS:
    search_novel_res = client.search_novel(word=search_word)
    print("search_novel", search_novel_res)

# no models
for search_word in SEARCH_WORDS:
    search_user_res = client.search_user(word=search_word)
    print("search_user", search_user_res)

# no models
illust_bookmark_detail_res = client.illust_bookmark_detail(BOOKMARKS_ILLUSTRATION_ID)
print("illust_bookmark_detail", illust_bookmark_detail_res)

# no models
illust_bookmark_add_res = client.illust_bookmark_add(BOOKMARKS_ILLUSTRATION_ID)
print("illust_bookmark_add", illust_bookmark_add_res)

# no models
illust_bookmark_delete_res = client.illust_bookmark_delete(BOOKMARKS_ILLUSTRATION_ID)
print("illust_bookmark_delete", illust_bookmark_delete_res)

# no models
user_follow_add_res = client.user_follow_add(BOOKMARKS_USER_ID)
print("user_follow_add", user_follow_add_res)

# no models
user_follow_delete_res = client.user_follow_delete(BOOKMARKS_USER_ID)
print("user_follow_delete", user_follow_delete_res)

# no models
user_edit_ai_show_settings_res = client.user_edit_ai_show_settings(setting="true")
print("user_edit_ai_show_settings", user_edit_ai_show_settings_res)

# no models
user_bookmark_tags_illust_res = client.user_bookmark_tags_illust(ENABLE_AI_SHOW_SETTINGS)
print("user_bookmark_tags_illust", user_bookmark_tags_illust_res)

# models
for user_id in USER_IDS:
    user_following_res = client.user_following(user_id=user_id)
    print("user_following", user_following_res)

# no models
for user_id in USER_IDS:
    user_follower_res = client.user_follower(user_id=user_id)
    print("user_follower", user_follower_res)

# no models
for user_id in USER_IDS:
    user_mypixiv_res = client.user_mypixiv(user_id=user_id)
    print("user_mypixiv", user_mypixiv_res)

# no models
for user_id in USER_IDS:
    user_list_res = client.user_list(user_id=user_id)
    print("user_list", user_list_res)

# no models
for ugoria_id in UGORIA_IDS:
    ugoira_metadata_res = client.ugoira_metadata(illust_id=ugoria_id)
    print("ugoira_metadata", ugoira_metadata_res)

# models
for user_id in USER_IDS:
    user_novels_res = client.user_novels(user_id=user_id)
    print("user_novels", user_novels_res)

# no models
for series_id in NOVEL_SERIES_IDS:
    novel_series_res = client.novel_series(series_id=series_id)
    print("novel_series", novel_series_res)

# models
for novel_id in NOVEL_IDS:
    novel_detail_res = client.novel_detail(novel_id=novel_id)
    print("novel_detail", novel_detail_res)

# no models
novel_new_res = client.novel_new()
print("novel_new", novel_new_res)

# no models
novel_follow_res = client.novel_follow()
print("novel_follow", novel_follow_res)

# models
for novel_id in NOVEL_IDS:
    webview_novel_res = client.webview_novel(novel_id=novel_id)
    print("webview_novel", webview_novel_res)

# models
for novel_id in NOVEL_IDS:
    novel_text_res = client.novel_text(novel_id=novel_id)
    print("novel_text", novel_text_res)

# no models
illust_new_res = client.illust_new()
print("illust_new", illust_new_res)

# no models
for showcase_article_id in SHOWCASE_ARTICLE_IDS:
    showcase_article_res = client.showcase_article(showcase_id=showcase_article_id)
    print("showcase_article", showcase_article_res)
