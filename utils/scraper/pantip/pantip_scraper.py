from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import time
import json


class PantipScraper:

    def __init__(self, chromedriver_path: str, chrome_headless: bool = True):
        self.chromedriver_path = chromedriver_path
        self.chrome_headless = chrome_headless
        # wait for page load
        self.sleep_time = 1

    def _initialize_driver(self):
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

        options = webdriver.ChromeOptions()

        if self.chrome_headless:
            options.add_argument("headless")

        self.driver = webdriver.Chrome(desired_capabilities=capabilities,
                                       executable_path=self.chromedriver_path,
                                       chrome_options=options)

    def _get_responses(self) -> list[dict]:
        logs_raw = self.driver.get_log("performance")
        logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
        responses = logs
        # override this function
        return responses

    def scrape(self):
        # override this function
        pass