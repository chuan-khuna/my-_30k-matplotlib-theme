from multiprocessing import Pool
from .save_utils import *
from .pantip_scraper import *
import pandas as pd
import numpy as np


def scrape_all_topics(keyword: str, max_page: int = 50):
    n_pages = get_number_of_topic_pages(keyword)
    if n_pages > max_page:
        n_pages = max_page

    data = []
    for page in range(1, n_pages + 1):
        res = scrape_topics(keyword, page)
        data += res['data']

    return data