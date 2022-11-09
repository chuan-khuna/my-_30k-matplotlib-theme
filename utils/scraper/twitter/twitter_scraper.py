import json
import re
import requests
import yaml


class TwitterScraper:

    def __init__(self, header_yml_path: str):
        """
        Args:
            header_yml_path (str): A YAML file that contains request header params
            it should contain (log in search) ['authorization', 'cookie', 'x-csrf-token'] (nov 2022)
            for incognito search it also need 'x-guest-token'
        """
        self.n_lazy_load = 10
        self.root_url = "https://twitter.com/i/api/2/search/adaptive.json"
        self.headers = self.__load_yaml_params(header_yml_path)

    def __format_keyword(self, keyword: str) -> str:
        return re.sub(r'\s', '%20', keyword)

    def __load_yaml_params(self, yaml_path: str) -> dict:

        with open(yaml_path) as f:
            params = yaml.load(f, yaml.Loader)

        return params

    def __create_payload(self, keyword: str, cursor_token: str) -> str:
        """Create GET request payload

        Args:
            keyword (str): keyword to search
            cursor_token (str): _description_

        Returns:
            str: _description_
        """

        if cursor_token:
            cursor_param = f"&cursor={cursor_token}"
        else:
            cursor_param = ''

        keyword_param = self.__format_keyword(keyword)

        payload = f"?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_ext_limited_action_results=false&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_ext_collab_control=true&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q={keyword_param}&count=20&query_source=typeahead_click{cursor_param}&pc=1&spelling_corrections=1&include_ext_edit_control=true&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CreplyvotingDownvotePerspective%2CvoiceInfo%2Cenrichments%2CsuperFollowMetadata%2CunmentionInfo%2CeditControl%2Ccollab_control%2Cvibe"

        return payload

    def _create_request_url(self, keyword: str, cursor_token: str) -> str:

        payload = self.__create_payload(keyword, cursor_token)
        if not payload.startswith('?'):
            payload = '?' + payload

        if self.root_url.endswith('?'):
            root_url = self.root_url[:-1]
        else:
            root_url = self.root_url

        return root_url + payload

    def _find_cursor_token(self, res_json: dict) -> str:
        str_json = json.dumps(res_json)
        tokens = re.findall(r"\"cursor\": \{\"value\": \"([a-zA-Z0-9_-]+)\"*", str_json)

        token = ''
        if len(tokens) != 0:
            token = tokens[0]

        return token

    def _scrape_one_lazy_load(self, keyword: str, cursor_token: str = ''):
        url = self._create_request_url(keyword, cursor_token)
        res = requests.get(url, headers=self.headers)

        if res.status_code == 200:
            return res.json()
        else:
            return {}

    def __flatten_dict(self, dict_: dict) -> list[dict]:
        """Flatten elements in the responses from {id: {..detail...}, id: {}} to [{..detail..}, {}]

        Args:
            dict_ (dict): `{id: detail, id: detail}` dict data from API response

        Returns:
            list[dict]: flattened data in `[detail, detail]` format
        """
        flattened = []
        for k, v in dict_.items():
            flattened.append(v)
        return flattened

    def scrape(self, keyword: str) -> dict[list[dict]]:
        """Scrape twitter data for a given keyword

        Returns:
            dict: list of tweets detail and list of users detail
        """

        tweets = []
        users = []
        cursor_token = ''
        for n in range(self.n_lazy_load):
            print(f"Lazy load page {n+1} ...")
            res = self._scrape_one_lazy_load(keyword, cursor_token)
            cursor_token = self._find_cursor_token(res)
            if 'globalObjects' not in res.keys():
                print("Cannot find data in json response")
                break
            page_n_tweets = self.__flatten_dict(res['globalObjects']['tweets'])
            page_n_users = self.__flatten_dict(res['globalObjects']['users'])
            print(f"> Found {len(page_n_tweets)} tweets")
            if len(page_n_tweets) == 0:
                break

            tweets += page_n_tweets
            users += page_n_users
        data = {'tweets': tweets, 'users': users}
        return data