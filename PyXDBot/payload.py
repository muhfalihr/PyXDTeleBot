from PyXDBot.utility import Proccessor
from typing import Any, Dict, Tuple

class BuilderPayloads:
     def __init__(self) -> Dict[str, Any]:
          '''
          Builder Payloads :
          :> UserByScreenName
          :> UserMedia
          :> TweetDetail
          '''
          self.FEATURES: Dict[str, bool] = {
                "responsive_web_graphql_exclude_directive_enabled": True,
                "verified_phone_label_enabled": False,
                "creator_subscriptions_tweet_preview_api_enabled": True,
                "responsive_web_graphql_timeline_navigation_enabled": True,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                "c9s_tweet_anatomy_moderator_badge_enabled": True,
                "tweetypie_unmention_optimization_enabled": True,
                "responsive_web_edit_tweet_api_enabled": True,
                "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                "view_counts_everywhere_api_enabled": True,
                "longform_notetweets_consumption_enabled": True,
                "responsive_web_twitter_article_tweet_consumption_enabled": False,
                "tweet_awards_web_tipping_enabled": False,
                "freedom_of_speech_not_reach_fetch_enabled": True,
                "standardized_nudges_misinfo": True,
                "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                "rweb_video_timestamps_enabled": True,
                "longform_notetweets_rich_text_read_enabled": True,
                "longform_notetweets_inline_media_enabled": True,
                "responsive_web_media_download_video_enabled": False,
                "responsive_web_enhance_cards_enabled": False
            }
     
     @Proccessor.payload
     def payload_UserByScreenName(self, **kwargs) -> Tuple[Dict]:
          '''
          builder payload for UserByScreenName
          '''
          variables: Dict[str, bool] = {
               "screen_name": kwargs["screen_name"].lower(),
                "withSafetyModeUserFields": True
          }
          features: Dict[str, bool] = {
                "hidden_profile_likes_enabled": True,
                "hidden_profile_subscriptions_enabled": True,
                "responsive_web_graphql_exclude_directive_enabled": True,
                "verified_phone_label_enabled": False,
                "subscriptions_verification_info_is_identity_verified_enabled": True,
                "subscriptions_verification_info_verified_since_enabled": True,
                "highlights_tweets_tab_ui_enabled": True,
                "responsive_web_twitter_article_notes_tab_enabled": False,
                "creator_subscriptions_tweet_preview_api_enabled": True,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                "responsive_web_graphql_timeline_navigation_enabled": True
            }
          fieldToggles: Dict[str, bool] = {"withAuxiliaryUserLabels": False}

          # Returns Tuple Values ​​with value Dictionary.
          return variables, features, fieldToggles
     
     @Proccessor.payload
     def payload_UserMedia(self, **kwargs):
          '''
          builder payload for UserMedia
          '''
          userId: str = kwargs.get("userId")
          count: int = kwargs.get("count", 20)
          cursor: str | None = kwargs.get("cursor", None)

          variables: Dict[str, bool] = {
                    "userId": f"{userId}",
                    "count": count,
                    "cursor": f"{cursor}",
                    "includePromotedContent": False,
                    "withClientEventToken": False,
                    "withBirdwatchNotes": False,
                    "withVoice": True,
                    "withV2Timeline": True
                } if cursor else {
                    "userId": f"{userId}",
                    "count": count,
                    "includePromotedContent": False,
                    "withClientEventToken": False,
                    "withBirdwatchNotes": False,
                    "withVoice": True,
                    "withV2Timeline": True
                }
          features: Dict[str, bool] = self.FEATURES

          # Returns Tuple Values ​​with value Dictionary.
          return variables, features
     
     @Proccessor.payload
     def payload_TweetDetail(self, **kwargs):
          '''
          builder payload for TweetDetail
          '''
          focalTweetId: str = kwargs.get("focalTweetId")
          controller_data: str = kwargs.get("controller_data", "DAACDAABDAABCgABAAAAAAAAAAAKAAkXK+YwNdoAAAAAAAA=")
          cursor: str | None = kwargs.get("cursor", None)

          variables: Dict[str, bool] = {
                    "focalTweetId": f"{focalTweetId}",
                    "cursor": f"{cursor}",
                    "referrer": "tweet",
                    "controller_data": f"{controller_data}",
                    "with_rux_injections": False,
                    "includePromotedContent": True,
                    "withCommunity": True,
                    "withQuickPromoteEligibilityTweetFields": True,
                    "withBirdwatchNotes": True,
                    "withVoice": True,
                    "withV2Timeline": True
                } if cursor else {
                    "focalTweetId": f"{focalTweetId}",
                    "with_rux_injections": False,
                    "includePromotedContent": True,
                    "withCommunity": True,
                    "withQuickPromoteEligibilityTweetFields": True,
                    "withBirdwatchNotes": True,
                    "withVoice": True,
                    "withV2Timeline": True
                }
          features: Dict[str, bool] = self.FEATURES
          fieldToggles: Dict[str, bool] = {"withArticleRichContentState": False}

          # Returns Tuple Values ​​with value Dictionary.
          return variables, features, fieldToggles
