from utils.scraper.twitter.new.tweet_scraper import TweetScraper
from unittest.mock import patch, MagicMock, Mock
import pytest
import requests
import os

# https://stackoverflow.com/questions/7165749/open-file-in-a-relative-location-in-python
TEST_PATH = os.path.dirname(__file__)
HEADER_PATH = os.path.join(TEST_PATH, "misc/twitter_header.yml")


@pytest.fixture
def scraper():
    print(HEADER_PATH)
    scraper = TweetScraper(HEADER_PATH)
    yield scraper
    del scraper


# This scraper scrape for tweets information
# ie from Twitter's search bar
def test_initialise_tweet_scraper_with_header_yaml():
    scraper = TweetScraper(HEADER_PATH)
    # test attributes
    scraper.max_lazyload
    scraper.api_url
    assert isinstance(scraper.headers, dict)


# mock twitter response
@patch('requests.get', return_value=requests.Response())
# an error occurs
@patch('requests.Response.json', side_effect=Exception)
def test_scrape_lazyload_should_return_blank_dict_if_error_occurs(m1, m2, scraper):
    result = scraper.scrape_lazyload('keyword', 'token')
    assert result == {}


# mock twitter response
expected_result = {'hello': 'world'}


@patch('requests.get', return_value=requests.Response())
# an error occurs
@patch('requests.Response.json', return_value=expected_result)
def test_scrape_lazyload_should_return_the_response_without_altering(m1, m2, scraper):
    result = scraper.scrape_lazyload('keyword', 'token')
    assert result == expected_result


def test_extract_token_should_return_none_if_error_or_cannot_token_doesnt_exist(scraper):
    # error occurs, blank response, cannot find token
    response = {}
    token = scraper.extract_token(response)
    assert token is None


def test_extract_token_should_return_token_as_str(scraper):
    # twiiter response here?
    response = {}
    token = scraper.extract_token(response)
    assert not isinstance(token, list)
    assert isinstance(token, str)


# todo: think about how this function should return
def test_process_response_should_return_something(scraper):
    pass


def test_scrape_function_should_loop_until_it_reach_limit(scraper):
    pass


# check if process(response) -> {}
# check if token is None
def test_scrape_function_should_break_the_loop_when_no_more_data(scraper):
    pass


def test_scrape_function_should_break_the_loop_if_token_is_none(scraper):
    pass


# test the funcion response type
def test_scrape_function_should_return_type_something(scraper):
    pass