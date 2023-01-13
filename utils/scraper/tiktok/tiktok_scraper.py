import pandas as pd
import json
import numpy as np
import yaml
from .tiktok_scraper_base import TiktokScraperBase
import requests


class TiktokScraper(TiktokScraperBase):

    def __init__(self, header_yaml: str):
        self.headers = self._load_header_from_yaml(header_yaml)

        self.api_url = "https://www.tiktok.com/api/search/general/full/"
        self.max_lazyload = 10
        self.lazyload_items = 12

        self.ms_token = 'OPQgC4-0aD7GYIZk2MAb48fj7NZ090vsmo_tPc8ZZNytrIy9U9M5bI6qXE8Z-R9w84OKNM9ZQTFKXxfkAIYuZS-toqLT6tizDHoU_YmIVR0Eua29kBkeb9P_161CnCcVMu-R-txLQxIiaqE='
        self.x_bogus = 'DFSzswVY73UANeIISZ1gl37TlqtC'
        self._signature = '_02B4Z6wo00001ozSw4wAAIDBGASYgoTNM76M0scAAMEB78'
        self.verifyFp = 'verify_lcu5mvmc_OMovJ8jM_4eGR_4FxH_Ay3V_tKmAKBizEvuj'
        self.region = 'TH'

    def _build_payload(self, keyword: str, offset: int) -> dict:
        payload = {
            'aid': 1988,
            'app_language': 'en',
            'app_name': 'tiktok_web',
            'battery_info': 1,
            'browser_language': 'en-GB',
            'browser_name': 'Mozilla',
            'browser_online': True,
            'channel': 'tiktok_web',
            'cookie_enabled': True,
            'device_platform': 'web_pc',
            'focus_state': True,
            'from_page': 'search',
            'history_len': 6,
            'is_fullscreen': False,
            'is_page_visible': True,
            'keyword': '',
            'offset': 0,
            'priority_region': None,
            'region': self.region,
            'screen_height': 1080,
            'screen_width': 1920,
            'tz_name': 'Asia/Bangkok',
            'verifyFp': self.verifyFp,
            'webcast_language': 'en',
            'msToken': self.ms_token,
            'X-Bogus': self.x_bogus,
            '_signature': self._signature,
        }

        payload['keyword'] = keyword
        payload['offset'] = offset
        return payload

    def process_response(self, response: dict) -> list[dict]:
        processed_data = []
        if response['status_code'] == 203:
            data = response['data']

            for d in data:
                try:
                    d = d['item']
                    processed_data.append(d)
                except Exception:
                    pass
        return processed_data

    def scrape_lazyload(self, keyword: str, offset: int) -> dict:
        payload = self._build_payload(keyword, offset)
        try:
            res = requests.get(self.api_url, params=payload, headers=self.headers, timeout=5)
            response_json = res.json()
        except Exception:
            response_json = {}

        return response_json

    def scrape(self, keyword: str) -> list[dict]:

        results = []

        for i in range(self.max_lazyload):
            offset = i * self.lazyload_items

            print(".", end="")
            if (i + 1) % 5 == 0:
                print(i + 1)

            res = self.scrape_lazyload(keyword, offset)

            if res == {}:
                break

            processed_res = self.process_response(res)
            results += processed_res

        return results