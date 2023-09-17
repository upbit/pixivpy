import json
import logging
import os

logger = logging.getLogger(__name__)

FIXTURES_DIR = "tests/fixtures"
JSON_FIXTURES_DIR = "tests/fixtures/json"


def load_data_from_file(filename):
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


def load_json_from_file(filename):
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
