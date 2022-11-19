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


def test_initialise_thread_scraper_with_header_yaml():
    scraper = ThreadScraper(HEADER_PATH)
    # test attributes
    scraper.max_lazyload
    scraper.api_url
    assert isinstance(scraper.headers, dict)


# mock twitter response
@patch('requests.get', return_value=requests.Response())
# an error occurs
@patch('requests.Response.json', side_effect=Exception)
def test_scrape_lazyload_should_return_blank_dict_if_error_occurs(m1, m2, scraper):
    result = scraper.scrape_lazyload('tweet_id', 'token')
    assert result == {}


# mock twitter response
expected_result = {'hello': 'world'}
response_mock = requests.Response()
response_mock.status_code = 200


@patch('requests.get', return_value=response_mock)
# an error occurs
@patch('requests.Response.json', return_value=expected_result)
def test_scrape_lazyload_should_return_the_response_without_altering(m1, m2, scraper):
    result = scraper.scrape_lazyload('tweet_id', 'token')
    assert result == expected_result


# mock twitter response
expected_result = {'hello': 'world'}
response_mock = requests.Response()
response_mock.status_code = 429


@patch('requests.get', return_value=response_mock)
# an error occurs
@patch('requests.Response.json', return_value=expected_result)
def test_scrape_lazyload_should_return_blank_dict_if_response_code_is_not_200(m1, m2, scraper):
    result = scraper.scrape_lazyload('tweet_id', 'token')
    assert result != expected_result
    assert result == {}


def test_extract_token_should_return_none_if_error_or_cannot_token_doesnt_exist(scraper):
    # error occurs, blank response, cannot find token
    response = {}
    token = scraper._extract_token(response)
    assert token is None


def test_extract_token_should_return_token_as_str(scraper):
    # twiiter response here?
    # load mock response
    with open(os.path.join(TEST_PATH, "misc/twitter/full_thread_response.json")) as f:
        response = json.load(f)
    token = scraper._extract_token(response)
    assert not isinstance(token, list)
    assert isinstance(token, str)
    # token is a long length string
    assert len(token) > 10


def test_process_response_should_return_a_list_of_dictionary_that_contains_a_reply_tweet_data(
        scraper):
    # processed_response = [{..rep1..}, {..rep2..}]
    with open(os.path.join(TEST_PATH, "misc/twitter/full_thread_response.json")) as f:
        mock_response = json.load(f)
    processed_response = scraper.process_response(mock_response)

    assert isinstance(processed_response, list)
    for item in processed_response:
        assert isinstance(item, dict)
