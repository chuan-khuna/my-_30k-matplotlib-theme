from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import time
import json


class PantipCommentsScraper:

    def __init__(self, chromedriver_path: str, chrome_headless: bool = True):
        self.chromedriver_path = chromedriver_path
        self.chrome_headless = chrome_headless
        self.sleep_time = 1

    def initialize_driver(self):
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

        options = webdriver.ChromeOptions()

        if self.chrome_headless:
            options.add_argument("headless")

        self.driver = webdriver.Chrome(desired_capabilities=capabilities,
                                       executable_path=self.chromedriver_path,
                                       chrome_options=options)

    def _get_comments_responses(self) -> list[dict]:

        # convert log to json/dict format
        logs_raw = self.driver.get_log("performance")
        logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

        comment_responses = []
        # filter only comments api
        # 'comment' in the api url
        for log in logs:
            if (log["method"] == "Network.responseReceived" and
                ("comment" in log["params"]["response"]["url"])):
                request_id = log["params"]["requestId"]
                comment_res = self.driver.execute_cdp_cmd("Network.getResponseBody",
                                                          {"requestId": request_id})
                comment_responses.append(json.loads(comment_res['body']))
        return comment_responses

    def _expand_all_pages(self):
        # find dropdown component to expand all comments
        dropdown_el = self.driver.find_element(By.CLASS_NAME, "dropdown-jump")
        select = Select(dropdown_el)
        n_options = len(dropdown_el.find_elements(By.XPATH, 'option'))
        for i in range(1, n_options):
            select.select_by_index(i)
            time.sleep(self.sleep_time)

    def scrape(self, url: str) -> list[dict]:
        self.initialize_driver()
        self.driver.get(url)
        time.sleep(self.sleep_time)
        self._expand_all_pages()
        comment_responses = self._get_comments_responses()
        self.driver.close()

        return comment_responses