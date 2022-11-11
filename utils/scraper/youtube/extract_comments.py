import re
import json


def _re_find_text(comment_thread_obj):
    """extract all {"text": "..."} from input obj as list of dict
    """

    # item from list in ["reloadContinuationItemsCommand"]["continuationItems"]
    text_data_str = re.findall(r"'contentText':\s+{'runs':\s+\[({.*})\]},\s+'publishedTimeText'",
                               str(comment_thread_obj))
    return [eval(t) for t in text_data_str]


def extract_comments_from_response(json_obj: dict) -> list[str]:
    """return all comments(str) in a lazy load response
    """

    extracted_comments = []

    if "onResponseReceivedEndpoints" in json_obj.keys():
        for continue_item in json_obj["onResponseReceivedEndpoints"]:

            # select key to dig deeper
            if "reloadContinuationItemsCommand" in continue_item.keys():
                k = "reloadContinuationItemsCommand"
            elif "appendContinuationItemsAction" in continue_item.keys():
                k = "appendContinuationItemsAction"
            # comments are in this key's list
            for comment_thread_item in continue_item[k]["continuationItems"]:
                if "commentThreadRenderer" in comment_thread_item.keys():
                    extracted_comments += _re_find_text(comment_thread_item)

    texts = []

    for comment in extracted_comments:
        # if no special characters
        if isinstance(comment, dict):
            texts.append(comment['text'])

        # if a comment contains special characters
        elif isinstance(comment, tuple):
            text = ''
            for item in comment:
                text += item['text']
            texts.append(text)

    return texts