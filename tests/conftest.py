import pytest


class ResponseFixture:
    def __init__(self, status_code, headers=None, json=None):
        self.status_code = status_code
        self.headers = headers or {}
        self.json = json or {}


@pytest.fixture
def pixiv_response_200():
    return ResponseFixture(status_code=200, headers=None, json=None)


@pytest.fixture
def pixiv_response_201():
    return ResponseFixture(status_code=201, headers=None, json=None)


@pytest.fixture
def pixiv_post_payload():
    # @TODO: enhance payload
    return {}


@pytest.fixture
def pixiv_url_common():
    # @TODO: enhance generating of Pixiv common url
    return "https://app-api.pixiv.net/v1/"


@pytest.fixture
def additional_headers_dict():
    return {"Keep-Alive": "timeout=5, max=1000"}


@pytest.fixture
def accept_language_header_dict():
    return {"Accept-Language": "en-us"}


@pytest.fixture
def valid_json_str():
    # TODO: simplify generating of valid json;
    #       move some data to files

    return """{
  "string": "string",
  "number": 1.0,
  "boolean": true,
  "array": [
    {
      "string": "string",
      "number": 1.0,
      "boolean": true
    },
    {
      "string": "string",
      "number": 1.0,
      "boolean": true
    }
  ],
  "null": null,
  "object": {
    "string": "string",
    "number": 1.0,
    "boolean": true
  }
}
"""


@pytest.fixture
def invalid_json_str():
    # TODO: simplify generating of valid json;
    #       move some data to files

    return """{
  'string': 'string',
}
"""
