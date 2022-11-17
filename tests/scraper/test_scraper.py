from utils.scraper.BaseScraper import BaseScraper
from unittest.mock import patch, MagicMock, Mock


@patch('requests.get', return_value={})
def test_scrape_lazyload_should_return_blank_dict_if_error_occur():
    # if an error occurs during requesting for json data, eg `requests.get` -- this function should return `{}`
    # then the other function will process the `{}` later
    scraper = BaseScraper()

    # if an error occurs, whilst scraping for something
    result = scraper.scrape_lazyload('url', 'token')
    assert result == {}
