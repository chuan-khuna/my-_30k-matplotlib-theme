from multiprocessing import Pool
from .save_utils import *
from .pantip_scraper import *
import pandas as pd
import numpy as np


def multithread_scrape(scraper, urls: list[str], save_path: str, pool_size: int = 4):
    with Pool(pool_size) as p:
        responses = p.map(scraper.scrape, urls)

    folders_ = [save_path] * len(responses)

    with Pool(pool_size) as p:
        p.starmap(save_comments_json, zip(responses, folders_))


def scrape_keyword(keyword_url: str, keyword: str, save_path: str, chromedriver_path: str):
    """Function to scrape a keyword and save output at `save_path`

    Args:
        keyword_url (str): keyword searching url from pantip
        keyword (str): output file name
        save_path (str): outout path (comments will be saved in /raw_comments/)
        chromedriver_path (str): chrome driver path
    """

    topic_file = save_path + f"{keyword}.json"

    comment_scraper = PantipCommentsScraper(chromedriver_path, True)
    topic_sraper = PantipTopicsScraper(chromedriver_path, True)

    topic_res = topic_sraper.scrape(keyword_url)
    save_topics_json(topic_res, keyword, save_path)

    with open(topic_file) as f:
        topic_res = json.load(f)

    topics_df = pd.DataFrame(topic_res)

    urls = topics_df['url']
    num_elems = len(urls)
    print(f"found {num_elems} topics")
    
    # batch + multithread scraping
    # for large size query
    batch_size = 32
    n_batches = int(np.ceil(num_elems / batch_size))
    for i in range(0, n_batches):
        if (end := (i + 1) * batch_size) > num_elems:
            end = num_elems
            batch_urls = urls[i * batch_size:]
        else:
            batch_urls = urls[i * batch_size:end]

        print(f"{i * batch_size}..{end}")
        multithread_scrape(comment_scraper, batch_urls, save_path)