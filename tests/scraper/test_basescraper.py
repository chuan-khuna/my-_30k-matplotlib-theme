from utils.scraper.scraper import Scraper
from unittest.mock import patch, MagicMock, Mock
import pytest
import requests

# To test that the most basic scrape function `scrape_lazyload`
# ie, scrape one page, scrape lazyload, scrape a pagination page
# It should get important information to build a request by `requests`
# It should handle error, ie return {}
# and if an error doesn't occur
# return a raw response conresponding to the request
# without altering/filtering any content


@pytest.fixture
def scraper():
    scraper = Scraper()
    yield scraper
    del scraper


def test_scraper_should_be_able_to_scrape(scraper):
    scraper.scrape()


def test_scraper_should_be_able_to_scrape_for_a_lazyload(scraper):
    scraper.scrape_lazyload()
