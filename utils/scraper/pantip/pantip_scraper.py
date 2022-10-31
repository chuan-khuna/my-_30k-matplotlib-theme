import requests
import json
import numpy as np


def _rotate_agent() -> str:
    agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    ]
    return np.random.choice(agents)


def scrape_comments_of_topic(topic_id: int, page: int) -> dict:
    """Scrape all comments data from a topic id
    Each page contains 100 comments

    Args:
        topic_id (int): _description_ 
        page (int): _description_

    Returns:
        dict: json response
    """
    url = "https://pantip.com/forum/topic/render_comments"
    agent = _rotate_agent()
    res = requests.get(url,
                       params={
                           'tid': topic_id,
                           'param': f'page{page}'
                       },
                       headers={
                           'x-requested-with': 'XMLHttpRequest',
                           'User-Agent': agent
                       })
    return json.loads(res.content)


def scrape_topics(keyword: str,
                  page: int = 1,
                  auth_token: str = "Basic dGVzdGVyOnRlc3Rlcg==") -> dict:
    """Scrape topics that contains a specified `keyword`
    each page contains 10 topics

    Args:
        keyword (str): a keyword to search for topics
        page (int, optional): _description_. Defaults to 1.
        auth_token (str, optional): _description_. Defaults to "Basic dGVzdGVyOnRlc3Rlcg==".

        To get auth_token:
        - request pantip search page for an arbitrary keyword
        - use Network tab of Chrome's inspect tool
        - Network > Fetch/XHR
        - find the api with name: 'getresult'

    Returns:
        dict: json response
    """

    url = "https://pantip.com/api/search-service/search/getresult"
    agent = _rotate_agent()
    res = requests.post(url,
                        headers={
                            'ptauthorize': auth_token,
                            'User-Agent': agent
                        },
                        json={
                            "keyword": keyword,
                            "page": page,
                            'rooms': [],
                            'timebias': False
                        })
    return json.loads(res.content)