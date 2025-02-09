import json
import logging
import os
import inspect
from typing import Any, Dict

logger = logging.getLogger(__name__)

FIXTURES_DIR = "tests/fixtures"
JSON_FIXTURES_DIR = "tests/fixtures/json"


class ResponseFixture:
    def __init__(
        self,
        status_code: int,
        headers: Dict[str, str] | None = None,
        json_data: Dict[str, Any] | None = None,
        text_data: str | None = None,
    ) -> None:
        self.status_code = status_code
        self.headers = headers or {}
        self.json = json_data or {}
        self.text = text_data or ""


def load_data_from_file(filename: str) -> str:
    try:
        with open(os.path.join(FIXTURES_DIR, filename)) as fp:
            return fp.read()
    except FileNotFoundError:
        logger.error(
            "Unable to read fixtures data from %s (`FIXTURES_DIR`: %s)",
            filename,
            FIXTURES_DIR,
        )
        raise


def load_json_from_file(filename: str) -> Any:
    try:
        with open(os.path.join(JSON_FIXTURES_DIR, filename)) as fp:
            return json.load(fp)
    except FileNotFoundError:
        logger.error(
            "Unable to read JSON fixtures from %s (`JSON_FIXTURES_DIR`: %s)",
            filename,
            JSON_FIXTURES_DIR,
        )
        raise


def load_func_mockjson() -> ResponseFixture:
    "load mock json by function nane"
    fname = inspect.stack()[1][3]
    filename = fname.replace("test_", "") + ".json"
    try:
        with open(os.path.join(JSON_FIXTURES_DIR, filename)) as fp:
            resp_text = fp.read()
            return ResponseFixture(
                status_code=200,
                headers={},
                json_data=json.loads(resp_text),
                text_data=resp_text,
            )
    except FileNotFoundError:
        logger.error(
            "Unable to read JSON fixtures from %s (`JSON_FIXTURES_DIR`: %s)",
            filename,
            JSON_FIXTURES_DIR,
        )
        raise
