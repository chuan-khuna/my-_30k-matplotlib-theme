from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import time
import json
from .pantip_scraper import PantipScraper


class PantipCommentsScraper(PantipScraper):

    def __init__(self, chromedriver_path: str, chrome_headless: bool = True):
        PantipScraper.__init__(self,
                               chromedriver_path=chromedriver_path,
                               chrome_headless=chrome_headless)

    def _get_responses(self) -> list[dict]:

        # convert log to json/dict format
        logs_raw = self.driver.get_log("performance")
        logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

        responses = []
        # filter only comments api
        # 'comment' in the api url
        for log in logs:
            if (log["method"] == "Network.responseReceived" and
                ("comment" in log["params"]["response"]["url"])):
                request_id = log["params"]["requestId"]
                response = self.driver.execute_cdp_cmd("Network.getResponseBody",
                                                       {"requestId": request_id})
                responses.append(json.loads(response['body']))
        return responses

    def _expand_all_pages(self):
        # find dropdown component to expand all comments
        dropdown_el = self.driver.find_element(By.CLASS_NAME, "dropdown-jump")
        select = Select(dropdown_el)
        n_options = len(dropdown_el.find_elements(By.XPATH, 'option'))
        for i in range(1, n_options):
            select.select_by_index(i)
            time.sleep(self.sleep_time)

    def scrape(self, url: str) -> list[dict]:
        self._initialize_driver()
        self.driver.get(url)
        time.sleep(self.sleep_time)
        self._expand_all_pages()
        comment_responses = self._get_responses()
        self.driver.close()

        return comment_responses