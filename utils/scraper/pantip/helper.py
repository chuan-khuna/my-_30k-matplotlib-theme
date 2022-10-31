from multiprocessing import Pool
from .save_utils import *
from .pantip_scraper import *
import pandas as pd
import numpy as np


def multithread_scrape_comments(scraper,
                                topic_ids: list[str | int],
                                save_path: str,
                                pool_size: int = 4):
    """Use multithreading(multiprocessing) to speed up scraping speed
    sprape for comments of multiple topics simultaneously

    Args:
        scraper (_type_): comment scrapers
        topic_ids (list[str  |  int]): a list of topic ids
        save_path (str): path to save comments json
        pool_size (int, optional): CPU's core to use. Defaults to 4.
    """

    # each element is a list of responses for a topic
    with Pool(pool_size) as p:
        responses = p.map(scraper.scrape, topic_ids)

    folder_ = [save_path] * len(responses)

    with Pool(pool_size) as p:
        p.starmap(save_comments_json, zip(responses, folder_))