class BaseScraper:
    # Parent class for all scrapers?

    def __init__(self):
        # initialise some setting
        # so that you can set created scrapers by using
        # scraper.max_lazyload = 10

        pass

    def extract_token(self, response: dict) -> str:
        token = response['token']
        return token

    def scrape_lazyload(self, keyword: str, token: str) -> dict:
        # return raw response
        # return {} if fail to request data (ie not 200 code)
        pass

    def process_response(self, response: dict) -> dict:
        # extract only important result
        # return {} if fail
        pass

    def save_json(self, json_obj: dict, path: str, filename: str):
        # a function for save raw files
        # create folder if not exist
        # save ...
        pass

    def scrape(self, keyword: str) -> list[dict]:
        # this function will scrape data until it reach the  limit

        cleaned_responses = []
        for i in range(10):
            # res = scrape_lazyload
            # process response
            # token
            # if something happends:
            # break
            # set variable for next lazy load
            pass

        return cleaned_responses
