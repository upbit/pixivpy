from __future__ import annotations

import json
import random
from typing import Any

import pytest

from tests.utils import ResponseFixture, load_data_from_file, load_json_from_file


@pytest.fixture
def pixiv_response_200() -> ResponseFixture:
    return ResponseFixture(status_code=200, headers=None, json_data=None)


@pytest.fixture
def pixiv_response_201() -> ResponseFixture:
    return ResponseFixture(status_code=201, headers=None, json_data=None)


@pytest.fixture
def pixiv_post_payload() -> dict[str, Any]:
    # @TODO: enhance payload
    return {}


@pytest.fixture
def pixiv_url_common() -> str:
    # @TODO: enhance generating of Pixiv common url
    return "https://app-api.pixiv.net/v1/"


@pytest.fixture
def pixiv_image_url() -> str:
    img_id = random.randint(100_000_000, 999_999_999)
    return f"https://i.pximg.net/c/600x1200_90/img-master/img/2023/01/01/12/38/38/{img_id}_p0_master1200.jpg"


@pytest.fixture
def additional_headers_dict() -> dict[str, str]:
    return {"Keep-Alive": "timeout=5, max=1000"}


@pytest.fixture
def accept_language_header_dict() -> dict[str, str]:
    return {"Accept-Language": "en-us"}


@pytest.fixture
def valid_json_str() -> str:
    json_data = load_json_from_file("general_valid_json.json")
    return json.dumps(json_data)


@pytest.fixture
def invalid_json_str() -> str:
    return load_data_from_file("general_invalid_json.txt")
