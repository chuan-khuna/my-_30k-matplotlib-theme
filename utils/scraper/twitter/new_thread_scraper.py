import json
import yaml
import requests
import re


class ThreadScraper:

    def __init__(self, header_yaml_path: str):
        self.max_lazyload = 10
        self.api_url = "https://twitter.com/i/api/graphql/BoHLKeBvibdYDiJON1oqTg/TweetDetail"
        self.headers = self._load_header_from_yaml(header_yaml_path)
        self.data_to_extract = ['tweets', 'users']

    def _load_header_from_yaml(self, yaml_path: str) -> dict:
        with open(yaml_path) as f:
            headers = yaml.load(f, yaml.Loader)
        return headers