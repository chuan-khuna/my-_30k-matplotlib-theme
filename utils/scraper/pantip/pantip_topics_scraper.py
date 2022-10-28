from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import time
import json
from .pantip_scraper import PantipScraper


class PantipTopicsScraper(PantipScraper):

    def __init__(self, chromedriver_path: str, chrome_headless: bool = True):
        PantipScraper.__init__(self,
                               chromedriver_path=chromedriver_path,
                               chrome_headless=chrome_headless)
        self.n_scrolls = 100
        self.scroll_wait = 1

    def _get_responses(self) -> list[dict]:

        # convert log to json/dict format
        logs_raw = self.driver.get_log("performance")
        logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

        responses = []
        # filter only topics api
        for log in logs:
            if ((log["method"] == "Network.responseReceived") and
                (("getresult" in log["params"]["response"]["url"]))):
                request_id = log["params"]["requestId"]
                response = self.driver.execute_cdp_cmd("Network.getResponseBody",
                                                       {"requestId": request_id})
                responses.append(json.loads(response['body']))
        return responses

    def _infinite_scroll(self):
        # action = ActionChains(self.driver)
        height = self.driver.execute_script("return document.body.scrollHeight")

        for i in range(self.n_scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.scroll_wait)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == height:
                break
            height = new_height

    def scrape(self, url: str) -> list[dict]:
        self._initialize_driver()
        self.driver.get(url)
        time.sleep(self.scroll_wait)
        self._infinite_scroll()
        responses = self._get_responses()
        self.driver.close()
        return responses