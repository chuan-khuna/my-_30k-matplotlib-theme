import json
import yaml
import requests
import re


class TweetScraper:

    def __init__(self, header_yaml_path: str):
        self.max_lazyload = 10
        self.api_url = "https://twitter.com/i/api/2/search/adaptive.json"
        self.headers = self._load_header_from_yaml(header_yaml_path)
        self.data_to_extract = ['tweets', 'users']

    def _load_header_from_yaml(self, yaml_path: str) -> dict:
        with open(yaml_path) as f:
            headers = yaml.load(f, yaml.Loader)
        return headers

    def _format_keyword(self, keyword: str) -> str:
        """Formatting to for url-safe string

        Args:
            keyword (str)

        Returns:
            str: url-safe string (ie string that appears in URLs)
        """
        keyword = re.sub(r"\s", "%20", keyword)
        return keyword

    def _build_payload(self, keyword: str, cursor_token: str) -> str:
        # see more: https://requests.readthedocs.io/en/latest/user/quickstart/
        # Passing Parameters In URLs (GET request)

        if cursor_token:
            cursor_param = f"&cursor={cursor_token}"
        else:
            cursor_param = ''

        keyword_param = self._format_keyword(keyword)

        payload = f"?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_ext_limited_action_results=false&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_ext_collab_control=true&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q={keyword_param}&count=20&query_source=typeahead_click{cursor_param}&pc=1&spelling_corrections=1&include_ext_edit_control=true&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CreplyvotingDownvotePerspective%2CvoiceInfo%2Cenrichments%2CsuperFollowMetadata%2CunmentionInfo%2CeditControl%2Ccollab_control%2Cvibe"

        return payload

    def _create_request_url(self, keyword: str, cursor_token: str):
        payload = self._build_payload(keyword, cursor_token)

        # ensure that there is only one '?'
        # only appears at a payload
        if not payload.startswith('?'):
            payload = '?' + payload

        if self.api_url.endswith('?'):
            api_url = self.api_url[:-1]
        else:
            api_url = self.api_url

        return api_url + payload

    def _extract_token(self, response: dict) -> str | None:
        """Extract cursor token from a raw response
        using regular expression because it is too deep to find
        TODO: update this code by finding token by condition

        Args:
            response (dict): raw response

        Returns:
            str | None: a string of cursor token, None if not exists
        """
        pattern = r"\"cursor\":\s+{\"cursorType\":\s+\"Bottom\",\s+\"value\":\s+\"([a-zA-Z0-9_-]+)\"}*"
        # sort_keys to ensure that string can be found by a regex pattern
        tokens = re.findall(pattern, json.dumps(response, sort_keys=True))

        if len(tokens) > 0:
            token = tokens[0]
        else:
            token = None

        return token

    def _flatten_dict(self, dict_: dict) -> list[dict]:
        return list(dict_.values())

    def process_response(self, response: dict) -> dict[str, list[dict]]:
        """Process raw response to extract only interested information

        Args:
            response (dict): raw response

        Returns:
            dict[list[dict]]: a dictionary where its keys is the information to extract, 
            eg `tweets`, `users`. Its values are a list of dicts of that entity.

            example {'tweets': [{...}, {...}], 'users': [{...}, {...}]}

            return {} if key not found
        """

        processed_data = {}
        if 'globalObjects' in response.keys():
            data = response['globalObjects']

            for k in self.data_to_extract:
                if k in data.keys():
                    processed_data[k] = self._flatten_dict(data[k])
                else:
                    processed_data[k] = []

        return processed_data

    def scrape_lazyload(self, keyword: str, cursor_token: str) -> dict:
        """Request for a lazyload response, return {} if error occurs

        Args:
            keyword (str): _description_
            cursor_token (str): _description_

        Returns:
            dict: raw json response
        """

        url = self._create_request_url(keyword, cursor_token)
        try:
            res = requests.get(url, headers=self.headers)

            if res.status_code == 200:
                response_json = res.json()
            else:
                response_json = {}
        except Exception:
            response_json = {}

        return response_json

    def scrape(self, keyword: str) -> dict[str, list[dict]]:
        """Scrape for tweets that contain a keyword from twitter (search bar)

        Args:
            keyword (str): _description_

        Returns:
            dict[str, list[dict]]: a dictionary where its keys is the information to extract, 
            eg `tweets`, `users`. Its values are a list of dicts of that entity.

            example {'tweets': [{...}, {...}], 'users': [{...}, {...}]}
        """

        # initialise cleaned data
        data = {}
        for k in self.data_to_extract:
            data[k] = []

        cursor_token = ''
        for i in range(1, self.max_lazyload + 1):
            print(f"Lazyload page: {i}")

            # request and process data
            res = self.scrape_lazyload(keyword, cursor_token)
            processed_data = self.process_response(res)
            cursor_token = self._extract_token(res)

            blank_response = True
            print("- Found", end=" ")
            for k in self.data_to_extract:
                if k in processed_data.keys():
                    data[k] += processed_data[k]
                    # if there is data in processed_data -> set flat to not break this loop
                    blank_response = blank_response and (len(processed_data[k]) == 0)
                    print(f"{k}: {len(processed_data[k])}", end=' ')
            print("")
            # check condition to break the loop
            # if 'globalObjects' not in res.keys():
            #     break
            if cursor_token is None:
                break
            if blank_response:
                break
        return data