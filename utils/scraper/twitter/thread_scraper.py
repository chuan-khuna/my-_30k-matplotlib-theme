import json
import re
import requests
import yaml


class ThreadScraper:

    def __init__(self, header_yaml_path: str):
        self.root_url = "https://twitter.com/i/api/graphql/BoHLKeBvibdYDiJON1oqTg/TweetDetail"
        self.headers = self.__load_yaml(header_yaml_path)
        self.n_lazy_load = 10

    def __load_yaml(self, path: str) -> dict:
        with open(path) as f:
            header = yaml.load(f, yaml.Loader)
        return header

    def __create_payload(self, tweet_id: str, cursor_token: str) -> str:
        """Create GET request payload, leading with `?`

        Args:
            tweet_id (str): _description_
            cursor_token (str): _description_

        Returns:
            str: _description_
        """

        if cursor_token:
            # URL-safe format of "cursor": "<token>",
            cursor_param = f"%22cursor%22%3A%22{cursor_token}%22%2C"
        else:
            cursor_param = ''

        path = f"?variables=%7B%22focalTweetId%22%3A%22{tweet_id}%22%2C{cursor_param}%22referrer%22%3A%22tweet%22%2C%22with_rux_injections%22%3Afalse%2C%22includePromotedContent%22%3Atrue%2C%22withCommunity%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withBirdwatchNotes%22%3Afalse%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withDownvotePerspective%22%3Atrue%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Atrue%7D&features=%7B%22responsive_web_twitter_blue_verified_badge_is_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22unified_cards_ad_metadata_container_dynamic_card_content_query_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_uc_gql_enabled%22%3Atrue%2C%22vibe_api_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Afalse%2C%22interactive_text_enabled%22%3Atrue%2C%22responsive_web_text_conversations_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Atrue%7D"

        return path

    def _create_request_url(self, tweet_id: str, cursor_token: str) -> str:
        payload = self.__create_payload(tweet_id, cursor_token)
        if not payload.startswith('?'):
            payload = '?' + payload

        if self.root_url.endswith('?'):
            root_url = self.root_url[:-1]
        else:
            root_url = self.root_url

        return root_url + payload

    def _find_cursor_token(self, response) -> str:
        tokens = []
        try:
            # get thread data; time line add
            thread_data = response['data']['threaded_conversation_with_injections_v2'][
                'instructions'][0]

            for entry in thread_data['entries']:
                try:
                    token = entry['content']['itemContent']['value']
                    tokens.append(token)
                except:
                    pass

        except KeyError:
            pass

        if len(tokens) > 0:
            token = tokens[0]
        else:
            token = ''
        return token

    def __get_replies_from_entry(self, thread_entry: dict) -> list[dict]:
        """Get all replies from an entry
        """

        replies = []
        try:
            thread_items = thread_entry['content']['items']
            for reply in thread_items:
                reply_tweet = reply['item']['itemContent']['tweet_results']['result']['legacy']
                replies.append(reply_tweet)
        except:
            pass
        return replies

    def _get_replies(self, response: dict) -> list[dict]:
        replies_in_one_lazyload = []
        try:
            thread_data = response['data']['threaded_conversation_with_injections_v2'][
                'instructions'][0]
            for entry in thread_data['entries']:
                replies = self.__get_replies_from_entry(entry)
                replies_in_one_lazyload += replies
        except:
            pass

        return replies_in_one_lazyload

    def _scrape_one_lazy_load(self, tweet_id: str, cursor_token: str = ''):
        url = self._create_request_url(tweet_id, cursor_token)
        res = requests.get(url, headers=self.headers, timeout=3)

        if res.status_code == 200:
            return res.json()
        else:
            print(res.status_code)
            return {}

    def scrape(self, tweet_id: str) -> list[dict]:
        replies = []
        cursor_token = ''
        for n in range(self.n_lazy_load):
            print(f"Lazy load page {n+1}")
            res = self._scrape_one_lazy_load(tweet_id, cursor_token)
            cursor_token = self._find_cursor_token(res)
            lazy_load_replies = self._get_replies(res)
            replies += lazy_load_replies
            print(f"> Found {len(lazy_load_replies)} replies")
            if len(lazy_load_replies) == 0:
                break
            if cursor_token == '':
                break
        return replies