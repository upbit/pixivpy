from unittest.mock import patch

from pixivpy3.api import BasePixivAPI


class TestBasePixivAPI(object):
    @patch("cloudscraper.create_scraper")
    def test_request_call_get(
        self, scraper_mock, pixiv_url_example, pixiv_response_200
    ):
        scraper_mock.return_value.get.return_value = pixiv_response_200

        api = BasePixivAPI()
        scraper_mock.assert_called_once()

        res = api.requests_call(method="GET", url=pixiv_url_example)
        assert res == pixiv_response_200

        scraper_mock.return_value.get.assert_called_once_with(
            pixiv_url_example, headers={}, params=None, stream=False
        )
