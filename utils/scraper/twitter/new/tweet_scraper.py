import json
import yaml
import requests
import re


class TweetScraper:

    def __init__(self, header_yaml_path: str):
        self.max_lazyload = 10
        self.api_url = "https://twitter.com/i/api/2/search/adaptive.json"
        self.headers = self._load_header_from_yaml(header_yaml_path)

    def _load_header_from_yaml(self, yaml_path: str) -> dict:
        with open(yaml_path) as f:
            headers = yaml.load(f, yaml.Loader)
        return headers

    def _build_payload(self, keyword: str, cursor_token: str) -> str:
        pass

    def scrape_lazyload(self) -> dict:
        pass