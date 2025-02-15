from __future__ import annotations

from unittest.mock import Mock, patch
from pixivpy3 import AppPixivAPI

from tests.utils import load_func_mockjson


class TestAppPixivAPI:
    @patch("cloudscraper.create_scraper")
    def test_illust_ranking(
        self,
        scraper_mock: Mock,
    ) -> None:
        scraper_mock.return_value.get.return_value = load_func_mockjson()

        api = AppPixivAPI()
        api.access_token = "test"
        scraper_mock.assert_called_once()

        json_result = api.illust_ranking("day", date="2025-02-04")
        assert json_result is not None

        # Check fields
        assert len(json_result.illusts) == 30

        illust = json_result.illusts[0]
        assert illust.id == 126839080
        assert illust.title == "奏鳴の宙"
        assert illust.caption == "「光る美少女展2024」出展作品"
        assert illust.image_urls.medium is not None
        assert illust.image_urls.large is not None
        assert illust.meta_single_page.original_image_url is not None
        assert illust.total_view == 79169

        # Check next url
        qs = api.parse_qs(json_result.next_url)
        assert qs["date"] == "2025-02-04"
        assert qs["offset"] == "30"  # parse from url should be str
