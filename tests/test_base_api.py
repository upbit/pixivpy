import json
from json import JSONDecodeError
from unittest.mock import patch

import pytest

from pixivpy3 import PixivError
from pixivpy3.api import BasePixivAPI


class TestBasePixivAPI:
    @patch("cloudscraper.create_scraper")
    def test_request_call_get(self, scraper_mock, pixiv_url_common, pixiv_response_200):
        scraper_mock.return_value.get.return_value = pixiv_response_200

        api = BasePixivAPI()
        scraper_mock.assert_called_once()

        res = api.requests_call(method="GET", url=pixiv_url_common)
        assert res == pixiv_response_200

        scraper_mock.return_value.get.assert_called_once_with(pixiv_url_common, headers={}, params=None, stream=False)

    @patch("cloudscraper.create_scraper")
    def test_request_call_post(self, scraper_mock, pixiv_url_common, pixiv_post_payload, pixiv_response_201):
        scraper_mock.return_value.post.return_value = pixiv_response_201

        api = BasePixivAPI()
        scraper_mock.assert_called_once()

        res = api.requests_call(method="POST", url=pixiv_url_common, data=pixiv_post_payload)
        assert res == pixiv_response_201

        scraper_mock.return_value.post.assert_called_once_with(
            pixiv_url_common,
            headers={},
            params=None,
            stream=False,
            data=pixiv_post_payload,
        )

    @patch("cloudscraper.create_scraper")
    def test_request_call_delete(self, scraper_mock, pixiv_url_common, pixiv_post_payload, pixiv_response_200):
        scraper_mock.return_value.delete.return_value = pixiv_response_200

        api = BasePixivAPI()
        scraper_mock.assert_called_once()

        res = api.requests_call(method="DELETE", url=pixiv_url_common, data=pixiv_post_payload)
        assert res == pixiv_response_200

        scraper_mock.return_value.delete.assert_called_once_with(
            pixiv_url_common,
            headers={},
            params=None,
            stream=False,
            data=pixiv_post_payload,
        )

    @patch("cloudscraper.create_scraper")
    def test_request_call_unknown_method(self, scraper_mock, pixiv_url_common, pixiv_response_200):
        scraper_mock.return_value.delete.return_value = pixiv_response_200

        api = BasePixivAPI()
        scraper_mock.assert_called_once()

        with pytest.raises(PixivError):
            api.requests_call(method="UNKNOWN", url=pixiv_url_common)

        scraper_mock.return_value.get.assert_not_called()
        scraper_mock.return_value.post.assert_not_called()
        scraper_mock.return_value.delete.assert_not_called()
        scraper_mock.return_value.options.assert_not_called()
        scraper_mock.return_value.head.assert_not_called()
        scraper_mock.return_value.put.assert_not_called()
        scraper_mock.return_value.patch.assert_not_called()

    @patch("cloudscraper.create_scraper")
    def test_set_accept_language(self, scraper_mock, accept_language_header_dict):
        api = BasePixivAPI()
        scraper_mock.assert_called_once()

        api.set_accept_language("en-us")

        for header, header_value in accept_language_header_dict.items():
            assert header in api.additional_headers
            assert api.additional_headers.get(header) == header_value

    @patch("cloudscraper.create_scraper")
    def test_set_additional_headers(self, scraper_mock, additional_headers_dict):
        api = BasePixivAPI()
        scraper_mock.assert_called_once()

        api.set_additional_headers(additional_headers_dict)

        for header, header_value in additional_headers_dict.items():
            assert header in api.additional_headers
            assert api.additional_headers.get(header) == header_value

    @patch("cloudscraper.create_scraper")
    def test_parse_json_valid(self, scraper_mock, valid_json_str):
        api = BasePixivAPI()
        scraper_mock.assert_called_once()

        res = api.parse_json(valid_json_str)
        assert json.loads(valid_json_str) == res

    @patch("cloudscraper.create_scraper")
    def test_parse_json_invalid(self, scraper_mock, invalid_json_str):
        api = BasePixivAPI()
        scraper_mock.assert_called_once()

        with pytest.raises(JSONDecodeError):
            api.parse_json(invalid_json_str)

    @patch("cloudscraper.create_scraper")
    def test_require_auth(self, scraper_mock):
        api = BasePixivAPI()
        scraper_mock.assert_called_once()

        assert api.access_token is None

        with pytest.raises(PixivError):
            api.require_auth()

    @patch("pixivpy3.api.open")
    @patch("pixivpy3.api.shutil")
    @patch("cloudscraper.create_scraper")
    def test_download(self, scraper_mock, shutil_mock, open_mock, pixiv_image_url, pixiv_response_200):
        api = BasePixivAPI()
        scraper_mock.assert_called_once()

        api.download(pixiv_image_url)

        scraper_mock.return_value.get.assert_called_once()
        assert pixiv_image_url in scraper_mock.return_value.get.call_args[0]
        assert scraper_mock.return_value.get.call_args[1].get("stream")

        shutil_mock.copyfileobj.assert_called_once_with(
            scraper_mock.return_value.get.return_value.__enter__.return_value.raw,
            open_mock.return_value.__enter__.return_value,
        )
