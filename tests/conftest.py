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
def pixiv_url_example():
    # @TODO: enhance url choices
    return "https://app-api.pixiv.net/v1/"
