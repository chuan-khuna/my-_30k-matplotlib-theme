# How to use scraper

last update: 1/Nov/2022

```py
# use this code in if __name__ == '__main__':

from utils.scraper.pantip.pantip_scraper import TopicScraper, CommentScraper
from utils.scraper.pantip.save_utils import *
from utils.scraper.pantip.helper import *
from dashboard_helper.data_preprocessing import *
from dashboard_helper.dataframe_utils import *

# dataset setting
keyword = "sawano"
keyword_file = "sawano"

# file paths
dataset_path = f"./data/{keyword_file}/"
topic_file = dataset_path + f"{keyword_file}.json"
comments_path = dataset_path + "/raw_comments/"

# initialise scraper
ts = TopicScraper()
ts.get_topic_detail = False
cs = CommentScraper()

# scrape data
print("Scrape data...save raw data to .json")
scrape_keyword(ts, cs, keyword, keyword_file, dataset_path)

# preprocess and save dataset file
print("Preprocess...save data to .csv")
raw_df = preprocess_keyword_data(topic_file, comments_path)
raw_df.to_csv(dataset_path + "raw_data.csv", index=False)

filtered_df = filter_keyword(raw_df, keyword)
filtered_melt_df = melt_dataframe(filtered_df)
filtered_melt_df.to_csv(dataset_path + "keyword_text.csv", index=False)

melt_df = melt_dataframe(raw_df)
melt_df.to_csv(dataset_path + "raw_text.csv", index=False)
```
