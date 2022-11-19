import json
import yaml
import requests
import re


class ThreadScraper:

    def __init__(self, header_yaml_path: str):
        self.max_lazyload = 10
        self.api_url = "https://twitter.com/i/api/graphql/BoHLKeBvibdYDiJON1oqTg/TweetDetail"
        self.headers = self._load_header_from_yaml(header_yaml_path)
        self.data_to_extract = ['tweets', 'users']

    def _load_header_from_yaml(self, yaml_path: str) -> dict:
        with open(yaml_path) as f:
            headers = yaml.load(f, yaml.Loader)
        return headers

    def _build_payload(self, tweet_id: str, cursor_token: str) -> dict:
        params = {
            "variables": {
                "focalTweetId": "1592481858520240128",
                # "cursor":
                #     "ZAAAAPAVHBmmgIDTwb-N0ZksgICq0aD6kZwsgIDUrZaT0ZkshsDS_aiEGwDRwNKBzYnRmSyCwNP9hi0AUcDT3dySJABA092lhhsA8AmA0-2Ni9GZLITA0fGshNGZLCUCEhUEAAA",
                "referrer": "tweet",
                "with_rux_injections": False,
                "includePromotedContent": True,
                "withCommunity": True,
                "withQuickPromoteEligibilityTweetFields": True,
                "withBirdwatchNotes": False,
                "withSuperFollowsUserFields": True,
                "withDownvotePerspective": True,
                "withReactionsMetadata": False,
                "withReactionsPerspective": False,
                "withSuperFollowsTweetFields": True,
                "withVoice": True,
                "withV2Timeline": True
            },
            "features": {
                "responsive_web_twitter_blue_verified_badge_is_enabled": True,
                "verified_phone_label_enabled": False,
                "responsive_web_graphql_timeline_navigation_enabled": True,
                "unified_cards_ad_metadata_container_dynamic_card_content_query_enabled": True,
                "tweetypie_unmention_optimization_enabled": True,
                "responsive_web_uc_gql_enabled": True,
                "vibe_api_enabled": True,
                "responsive_web_edit_tweet_api_enabled": True,
                "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                "standardized_nudges_misinfo": True,
                "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": False,
                "interactive_text_enabled": True,
                "responsive_web_text_conversations_enabled": False,
                "responsive_web_enhance_cards_enabled": True
            }
        }

        params["variables"]["focalTweetId"] = tweet_id
        
        if cursor_token:
            params["variables"]["cursor"] = cursor_token

        return params