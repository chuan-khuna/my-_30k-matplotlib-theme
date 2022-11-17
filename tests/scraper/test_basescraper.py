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


@pytest.fixture
def scraper():
    scraper = BaseScraper()
    yield scraper
    del scraper


@patch('requests.get', return_value=requests.Response())
@patch('requests.Response.json', side_effect=Exception)
def test_scrape_lazyload_should_return_blank_dictionary_if_error_occurs(m1, m2, scraper):
    res = scraper.scrape_lazyload('url', 'token')
    assert res == {}


mock_response = {'hello': {'world': 'python'}}


@patch('requests.get', return_value=requests.Response())
@patch('requests.Response.json', return_value=mock_response)
def test_scrape_lazyload_should_not_alter_raw_response(m1, m2):
    res = scraper.scrape_lazyload('url', 'token')
    assert res == mock_response


# suppose that an error occurs during finding a token
# the later function will check if token is none it will stop the process
@patch('requests.get', side_effect=Exception)
def test_extract_token_should_return_none_if_error_occurs_or_cannot_find_token(m1, scraper):
    response = {}
    token = scraper.extract_token(response)
    assert token is None


def test_extract_token_should_return_non_list_object(scraper):
    response = {'token': 'ThisIsToken'}
    token = scraper.extract_token(response)
    assert token == 'ThisIsToken'
    assert not isinstance(token, list)