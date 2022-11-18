from utils.scraper.twitter.tweet_scraper import TweetScraper
from unittest.mock import patch, MagicMock, Mock
import pytest
import requests
import os
import json

# https://stackoverflow.com/questions/7165749/open-file-in-a-relative-location-in-python
TEST_PATH = os.path.dirname(__file__)
HEADER_PATH = os.path.join(TEST_PATH, "misc/twitter/twitter_header.yml")
MOCK_PACKAGE_PATH = "utils.scraper.twitter.tweet_scraper.TweetScraper"


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
response_mock = requests.Response()
response_mock.status_code = 200


@patch('requests.get', return_value=response_mock)
# an error occurs
@patch('requests.Response.json', return_value=expected_result)
def test_scrape_lazyload_should_return_the_response_without_altering(m1, m2, scraper):
    result = scraper.scrape_lazyload('keyword', 'token')
    assert result == expected_result


# mock twitter response
expected_result = {'hello': 'world'}
response_mock = requests.Response()
response_mock.status_code = 429


@patch('requests.get', return_value=response_mock)
# an error occurs
@patch('requests.Response.json', return_value=expected_result)
def test_scrape_lazyload_should_return_blank_dict_if_response_code_is_not_200(m1, m2, scraper):
    result = scraper.scrape_lazyload('keyword', 'token')
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
    with open(os.path.join(TEST_PATH, "misc/twitter/tweet_cursor_token.json")) as f:
        response = json.load(f)
    expected_result = "Sawano-Hiroyuki-is-the-best-music-composer"
    token = scraper._extract_token(response)
    assert not isinstance(token, list)
    assert isinstance(token, str)
    assert token == expected_result


def test_flatten_dict_should_return_a_list_of_dicts(scraper):
    # example of twitter response format
    tweets = {'t1': {'content': 't1'}, 't2': {'content': 't2'}}

    result = scraper._flatten_dict(tweets)

    assert isinstance(result, list)
    for i, (_, v) in enumerate((tweets.items())):
        assert isinstance(result[i], dict)
        assert result[i] == v


def test_process_response_should_return_a_dictionary_with_tweets_and_users(scraper):
    # expected_response = {'users': [{...}, {...}], 'tweets': [{...}, {...}]}
    # type dict[list[dict]]
    # load mock response
    with open(os.path.join(TEST_PATH, "misc/twitter/full_tweets_response.json")) as f:
        mock_response = json.load(f)
    processed_response = scraper.process_response(mock_response)

    assert isinstance(processed_response, dict)
    assert isinstance(processed_response["tweets"], list)
    assert isinstance(processed_response["users"], list)


# there are things to stop the scrape function
# loop until it reachs max_lazyload limit
# response contains no data, ie cannot find some key in json
# response contains blank tweets, users
# cursor is None
tokens = ['token1', 'token2', None, None]
with open(os.path.join(TEST_PATH, "misc/twitter/full_tweets_response.json")) as f:
    mock_response = json.load(f)
mock_processed_data = {'tweets': [{'t1': 't1 content'}], 'users': [{'u1': 'u1 name'}]}


@patch(f'{MOCK_PACKAGE_PATH}._extract_token', side_effect=tokens)
@patch(f'{MOCK_PACKAGE_PATH}.scrape_lazyload', side_effect=[mock_response] * len(tokens))
@patch(f'{MOCK_PACKAGE_PATH}.process_response', side_effect=[mock_processed_data] * len(tokens))
def test_scrape_should_stop_when_cursor_token_is_none(m1, m2, m3, scraper):
    result = scraper.scrape('Sawano Hiroyuki')

    # count the number of loop
    # function should added data before break
    # if any error occurs, add []
    assert len(result['tweets']) == 3
    assert len(result['users']) == 3


# if data larger than limited page
total_lazyload = 15
tokens = ['token'] * total_lazyload
with open(os.path.join(TEST_PATH, "misc/twitter/full_tweets_response.json")) as f:
    mock_response = json.load(f)
mock_processed_data = {'tweets': [{'t1': 't1 content'}], 'users': [{'u1': 'u1 name'}]}


@patch(f'{MOCK_PACKAGE_PATH}._extract_token', side_effect=tokens)
@patch(f'{MOCK_PACKAGE_PATH}.scrape_lazyload', side_effect=[mock_response] * len(tokens))
@patch(f'{MOCK_PACKAGE_PATH}.process_response', side_effect=[mock_processed_data] * len(tokens))
def test_scrape_function_should_loop_until_it_reach_limit(m1, m2, m3, scraper):
    max_lazyload = 3
    scraper.max_lazyload = max_lazyload
    result = scraper.scrape('Sawano Hiroyuki')
    assert len(result['tweets']) == max_lazyload
    assert len(result['users']) == max_lazyload


# if data larger than limited page
total_lazyload = 15
tokens = ['token'] * total_lazyload
with open(os.path.join(TEST_PATH, "misc/twitter/full_tweets_response.json")) as f:
    mock_response = json.load(f)
mock_processed_data = {'tweets': [{'t1': 't1 content'}], 'users': [{'u1': 'u1 name'}]}


@patch(f'{MOCK_PACKAGE_PATH}._extract_token', side_effect=tokens)
@patch(f'{MOCK_PACKAGE_PATH}.scrape_lazyload',
       side_effect=[mock_response] * (len(tokens) - 1) + [{}])
@patch(f'{MOCK_PACKAGE_PATH}.process_response',
       side_effect=[mock_processed_data] * (len(tokens) - 1) + [{}])
def test_scrape_function_should_stop_the_loop_if_no_more_data(m1, m2, m3, scraper):
    max_lazyload = 20
    scraper.max_lazyload = max_lazyload
    result = scraper.scrape('Sawano Hiroyuki')
    # last page doesn't contain data
    assert len(result['tweets']) == total_lazyload - 1
    assert len(result['users']) == total_lazyload - 1