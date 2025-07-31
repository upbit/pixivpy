# This file contains test data for test_web_api.py

# Base URL for mocking
AJAX_BASE_URL = "https://www.pixiv.net/ajax"

# Sample User ID from the example file
TEST_USER_ID = 9153585

# Example response for the short user info endpoint
EXAMPLE_USER_INFO_SHORT_RESPONSE = {
    "error": False,
    "message": "",
    "body": {
        "userId": "9153585",
        "name": "haku89",
        "image": "https://i.pximg.net/user-profile/img/2018/06/26/14/26/03/14408330_3de67ff59732d611d71369bddd8ea287_50.jpg",
        "imageBig": "https://i.pximg.net/user-profile/img/2018/06/26/14/26/03/14408330_3de67ff59732d611d71369bddd8ea287_170.jpg",
        "premium": True,
        "isFollowed": False,
        "isMypixiv": False,
        "isBlocking": False,
        "background": None,
        "sketchLiveId": None,
        "partial": 0,
        "acceptRequest": False,
        "sketchLives": [],
    },
}

# Example response for the full user info endpoint
EXAMPLE_USER_INFO_FULL_RESPONSE = {
    "error": False,
    "message": "",
    "body": {
        "userId": "9153585",
        "name": "haku89",
        "image": "https://i.pximg.net/user-profile/img/2018/06/26/14/26/03/14408330_3de67ff59732d611d71369bddd8ea287_50.jpg",
        "imageBig": "https://i.pximg.net/user-profile/img/2018/06/26/14/26/03/14408330_3de67ff59732d611d71369bddd8ea287_170.jpg",
        "premium": True,
        "isFollowed": False,
        "isMypixiv": False,
        "isBlocking": False,
        "background": None,
        "sketchLiveId": None,
        "partial": 1,
        "acceptRequest": False,
        "sketchLives": [],
        "following": 349,
        "followedBack": False,
        "comment": "コメントや評価とタグ編集、いいね、ブックマークありがとうございます！\r\nhakuです。よろしく！\r\n日本語おk、English ok\r\n興味で絵を描いて生きています、\r\n\r\nFANBOX:https://haku89.fanbox.cc/\r\ntwitter：https://twitter.com/real_haku89\r\nご依頼連絡先：mak0hitachi89@gmail.com",
        "commentHtml": 'コメントや評価とタグ編集、いいね、ブックマークありがとうございます！<br />hakuです。よろしく！<br />日本語おk、English ok<br />興味で絵を描いて生きています、<br /><br />FANBOX:<a href="https://haku89.fanbox.cc/" target="_blank">https://haku89.fanbox.cc/</a><br />twitter：<strong><a href="https://twitter.com/real_haku89" target="_blank">twitter/real_haku89</a></strong><br />ご依頼連絡先：mak0hitachi89@gmail.com',
        "webpage": None,
        "social": {"twitter": {"url": "https://twitter.com/real_haku89"}},
        "canSendMessage": True,
        "region": {
            "name": "日本",
            "region": "JP",
            "prefecture": "26",
            "privacyLevel": "0",
        },
        "age": {"name": "23歳", "privacyLevel": "0"},
        "birthDay": {"name": "12月16日", "privacyLevel": "0"},
        "gender": {"name": "女性", "privacyLevel": "0"},
        "job": {"name": "教員", "privacyLevel": "0"},
        "workspace": {
            "userWorkspacePc": "RTX 3090+Ryzen5800X",
            "userWorkspaceTool": "CSP",
            "userWorkspaceTablet": "Cintiq DTH-1620",
            "userWorkspaceMouse": "大きくて可愛くないマウス",
            "userWorkspaceDesktop": "お茶",
            "userWorkspaceMusic": "ピアノ",
            "userWorkspaceDesk": "小さくてちょっと低い",
            "userWorkspaceChair": "大きな椅子",
        },
        "official": False,
        "group": [
            {
                "id": "3282",
                "title": "【中国語的群組!!】",
                "iconUrl": "https://i.pximg.net/c/128x128/imgaz/2012/09/12/23/08/46/group_icon_3282_square1200.jpg",
            },
            {
                "id": "13002",
                "title": "艦これpixiv鎮守府(紹介文(含補足事項)必読)",
                "iconUrl": "https://i.pximg.net/c/128x128/imgaz/2014/10/06/11/58/14/group_icon_13002_square1200.jpg",
            },
            {
                "id": "1514",
                "title": "iPadお絵描き会",
                "iconUrl": "https://i.pximg.net/c/128x128/imgaz/2012/05/27/01/10/25/group_icon_1514_square1200.jpg",
            },
            {
                "id": "11313",
                "title": "漫画どう描く？",
                "iconUrl": "https://s.pximg.net/common/images/group_no_icon.png",
            },
        ],
    },
}
