import json
import random

import pytest

from tests.utils import load_data_from_file, load_json_from_file


class ResponseFixture:
    def __init__(self, status_code, headers=None, json_data=None):
        self.status_code = status_code
        self.headers = headers or {}
        self.json = json_data or {}


@pytest.fixture
def pixiv_response_200():
    return ResponseFixture(status_code=200, headers=None, json_data=None)


@pytest.fixture
def pixiv_response_201():
    return ResponseFixture(status_code=201, headers=None, json_data=None)


@pytest.fixture
def pixiv_post_payload():
    # @TODO: enhance payload
    return {}


@pytest.fixture
def pixiv_url_common():
    # @TODO: enhance generating of Pixiv common url
    return "https://app-api.pixiv.net/v1/"


@pytest.fixture
def pixiv_image_url():
    return (
        "https://i.pximg.net/c/600x1200_90/img-master/"
        "img/2023/01/01/12/38/38/{}_p0_master1200.jpg".format(
            random.randint(100_000_000, 999_999_999)
        )
    )


@pytest.fixture
def additional_headers_dict():
    return {"Keep-Alive": "timeout=5, max=1000"}


@pytest.fixture
def accept_language_header_dict():
    return {"Accept-Language": "en-us"}


@pytest.fixture
def valid_json_str():
    json_data = load_json_from_file("general_valid_json.json")
    return json.dumps(json_data)


@pytest.fixture
def invalid_json_str():
    invalid_json_data = load_data_from_file("general_invalid_json.txt")
    return invalid_json_data
