from utils.scraper.BaseScraper import BaseScraper
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


@pytest.fixture(autouse=True)
def scraper():
    scraper = BaseScraper()
    yield scraper
    del scraper


@patch('requests.get', return_value=requests.Response())
@patch('requests.Response.json', side_effect=Exception)
def test_scrape_lazyload_should_return_blank_dictionary_if_error_occurs(m1, m2):
    res = scraper.scrape_lazyload('url', 'token')
    assert res == {}


mock_response = {'hello': {'world': 'python'}}


@patch('requests.get', return_value=requests.Response())
@patch('requests.Response.json', return_value=mock_response)
def test_scrape_lazyload_should_not_alter_raw_response(m1, m2):
    res = scraper.scrape_lazyload('url', 'token')
    assert res == mock_response