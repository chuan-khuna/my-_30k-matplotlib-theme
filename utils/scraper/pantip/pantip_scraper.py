import requests
import json
import random
import re
import numpy as np
from bs4 import BeautifulSoup
import time


class PantipScraper:

    def __init__(self, auth_token: str = "Basic dGVzdGVyOnRlc3Rlcg=="):
        self.auth_token = auth_token

    def _rotate_agent(self) -> str:
        # time.sleep(np.random.randint(1, 4))
        agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        ]
        return random.choice(agents)


class TopicScraper(PantipScraper):

    def __init__(self):
        PantipScraper.__init__(self)
        self.max_topic_page = 50
        self.api = "https://pantip.com/api/search-service/search/getresult"
        self.get_topic_detail = False

    def _scrape_topic_detail(self, topic_id: str | int):
        url = f"https://pantip.com/topic/{topic_id}"
        res = requests.get(url, headers={'User-Agent': self._rotate_agent()})
        soup = BeautifulSoup(res.content)
        topic_soup = soup.find(attrs={'class': "display-post-wrapper main-post type"})
        topic_detail = topic_soup.find(attrs={'class': "display-post-story"}).text
        return topic_detail

    def _scrape_one_page(self, keyword: str, page: int = 1) -> dict:
        agent = self._rotate_agent()
        res = requests.post(self.api,
                            headers={
                                'ptauthorize': self.auth_token,
                                'User-Agent': agent
                            },
                            json={
                                "keyword": keyword,
                                "page": page,
                                'rooms': [],
                                'timebias': False
                            })

        # when search a keyword by using this api
        # if the keyword is not in the topic's detail
        # 'detail' will not included in the response
        topics = json.loads(res.content)
        if self.get_topic_detail:
            for i, topic in enumerate(topics['data']):
                detail = self._scrape_topic_detail(topic['id'])
                topics['data'][i]['detail'] = detail
        return topics

    def _get_number_of_topic_pages(self,
                                   keyword: str,
                                   per_page: int = 10,
                                   max_page: int = 1000) -> int:
        # request to get the total number of topics
        res = self._scrape_one_page(keyword, 1)
        n_topic = res['total'].split(" ")[1]
        n_topic = int(re.sub(",", "", n_topic))
        print(f"found {n_topic} topics")
        n_page = int(np.ceil(n_topic / per_page))
        print(f"={n_page} pages of {per_page}topic/page")

        if self.max_topic_page < n_page:
            print(f"scrape only: {self.max_topic_page}")
            n_page = self.max_topic_page

        return n_page

    def scrape(self, keyword: str) -> list[dict]:
        """Get all topics for a given keyword

        Args:
            keyword (str): keyword to search

        Returns:
            list[dict]: list of pagination json API responses (raw)
        """

        total_pages = self._get_number_of_topic_pages(keyword)
        # limit the number of page to scrape
        n_pages = total_pages
        if n_pages > self.max_topic_page:
            n_pages = self.max_topic_page

        data = []
        for page in range(1, n_pages + 1):
            res = self._scrape_one_page(keyword, page)
            data.append(res)
        return data


class CommentScraper(PantipScraper):

    def __init__(self):
        self.api = "https://pantip.com/forum/topic/render_comments"

    def _scrape_one_page(self, topic_id: str | int, page: int = 1) -> dict:
        agent = self._rotate_agent()
        res = requests.get(self.api,
                           params={
                               'tid': topic_id,
                               'param': f'page{page}'
                           },
                           headers={
                               'x-requested-with': 'XMLHttpRequest',
                               'User-Agent': agent
                           })
        return json.loads(res.content)

    def _get_number_of_comment_pages(self, topic_id: str | int) -> int:
        res = self._scrape_one_page(topic_id)
        max_comments = res['paging']['max_comments']
        num_page = int(np.ceil(max_comments / 100))
        return num_page

    def scrape(self, topic_id: str | int) -> list[dict]:
        """Get all comment for a topic

        Args:
            topic_id (str | int): Topic ID can be either in or string

        Returns:
            list[dict]: list of pagination json API responses (raw)
        """
        n_pages = self._get_number_of_comment_pages(topic_id)
        data = []
        for page in range(1, n_pages + 1):
            res = self._scrape_one_page(topic_id, page)
            data.append(res)
        return data