from utils.scraper.twitter.new_thread_scraper import ThreadScraper
from unittest.mock import patch, MagicMock, Mock
import pytest
import requests
import os
import json

# https://stackoverflow.com/questions/7165749/open-file-in-a-relative-location-in-python
TEST_PATH = os.path.dirname(__file__)
HEADER_PATH = os.path.join(TEST_PATH, "misc/twitter/twitter_header.yml")
MOCK_PACKAGE_PATH = "utils.scraper.twitter.new_thread_scraper.ThreadScraper"


@pytest.fixture
def scraper():
    print(HEADER_PATH)
    scraper = ThreadScraper(HEADER_PATH)
    yield scraper
    del scraper