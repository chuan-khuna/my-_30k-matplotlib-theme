import json


def save_comments_json(scrape_result: list[dict], output_folder: str = "."):
    comments = []
    topic_id = scrape_result[0]['paging']['topic_id']

    for batch in scrape_result:
        if 'comments' in batch.keys():
            comments += batch['comments']

    output_file = f"{output_folder}/{topic_id}.json"
    with open(output_file, "w") as f:
        f.write(json.dumps(comments, ensure_ascii=False, indent=2))


def save_topics_json(keyword: str, scrape_result: list[dict], output_folder: str = "."):
    topics = []

    for batch in scrape_result:
        if 'data' in batch.keys():
            topics += batch['data']

    output_file = f"{output_folder}/{keyword}.json"
    with open(output_file, "w") as f:
        f.write(json.dumps(topics, ensure_ascii=False, indent=2))