from utility import Proccessor

class BuilderPayloads:
     def __init__(self) -> None:
          '''
          Builder Payloads :
          :> UserByScreenName
          :> UserMedia
          :> TweetDetail
          '''
          self.FEATURES = {
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
     def payload_UserByScreenName(self, **kwargs):
          '''
          builder payload for UserByScreenName
          '''
          variables = {
               "screen_name": kwargs["screen_name"].lower(),
                "withSafetyModeUserFields": True
          }
          features = {
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
          fieldToggles = {"withAuxiliaryUserLabels": False}
          return variables, features, fieldToggles
     
     @Proccessor.payload
     def payload_UserMedia(self, **kwargs):
          '''
          builder payload for UserMedia
          '''
          userId = kwargs.get("userId")
          count = kwargs.get("count", 20)
          cursor = kwargs.get("cursor", None)

          variables = {
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
          features = self.FEATURES
          return variables, features
     
     @Proccessor.payload
     def payload_TweetDetail(self, **kwargs):
          '''
          
          '''
          focalTweetId = kwargs.get("focalTweetId")
          controller_data = kwargs.get("controller_data", "DAACDAABDAABCgABAAAAAAAAAAAKAAkXK+YwNdoAAAAAAAA=")
          cursor = kwargs.get("cursor", None)

          variables = {
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
          features = self.FEATURES
          fieldToggles = {"withArticleRichContentState": False}
          return variables, features, fieldToggles

# def __buildpayload(self, **kwargs) -> dict:
#         self.__logger.info("Building payloads")

#         func_name = kwargs["func_name"]
#         match func_name:
#             case "get_rest_id":
#                 screen_name = kwargs["screen_name"]

#                 variables = {
#                     "screen_name": screen_name.lower(),
#                     "withSafetyModeUserFields": True
#                 }

#                 fieldToggles = {"withAuxiliaryUserLabels": False}

#             case "__tweetdetail":
#                 focalTweetId = kwargs["focalTweetId"]
#                 controller_data = kwargs["controller_data"]
#                 cursor = kwargs["cursor"]

                # variables = {
                #     "focalTweetId": f"{focalTweetId}",
                #     "cursor": f"{cursor}",
                #     "referrer": "tweet",
                #     "controller_data": f"{controller_data}",
                #     "with_rux_injections": False,
                #     "includePromotedContent": True,
                #     "withCommunity": True,
                #     "withQuickPromoteEligibilityTweetFields": True,
                #     "withBirdwatchNotes": True,
                #     "withVoice": True,
                #     "withV2Timeline": True
                # } if cursor else {
                #     "focalTweetId": f"{focalTweetId}",
                #     "with_rux_injections": False,
                #     "includePromotedContent": True,
                #     "withCommunity": True,
                #     "withQuickPromoteEligibilityTweetFields": True,
                #     "withBirdwatchNotes": True,
                #     "withVoice": True,
                #     "withV2Timeline": True
                # }

#                 fieldToggles = {"withArticleRichContentState": False}

            # case "allmedia" | "images":
            #     userId = kwargs["userId"]
            #     count = kwargs["count"]
            #     cursor = kwargs["cursor"]

            #     variables = {
            #         "userId": f"{userId}",
            #         "count": count,
            #         "cursor": f"{cursor}",
            #         "includePromotedContent": False,
            #         "withClientEventToken": False,
            #         "withBirdwatchNotes": False,
            #         "withVoice": True,
            #         "withV2Timeline": True
            #     } if cursor else {
            #         "userId": f"{userId}",
            #         "count": count,
            #         "includePromotedContent": False,
            #         "withClientEventToken": False,
            #         "withBirdwatchNotes": False,
            #         "withVoice": True,
            #         "withV2Timeline": True
            #     }

#         payload = {
#             "variables": variables,
            # "features": {
            #     "responsive_web_graphql_exclude_directive_enabled": True,
            #     "verified_phone_label_enabled": False,
            #     "creator_subscriptions_tweet_preview_api_enabled": True,
            #     "responsive_web_graphql_timeline_navigation_enabled": True,
            #     "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            #     "c9s_tweet_anatomy_moderator_badge_enabled": True,
            #     "tweetypie_unmention_optimization_enabled": True,
            #     "responsive_web_edit_tweet_api_enabled": True,
            #     "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            #     "view_counts_everywhere_api_enabled": True,
            #     "longform_notetweets_consumption_enabled": True,
            #     "responsive_web_twitter_article_tweet_consumption_enabled": False,
            #     "tweet_awards_web_tipping_enabled": False,
            #     "freedom_of_speech_not_reach_fetch_enabled": True,
            #     "standardized_nudges_misinfo": True,
            #     "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            #     "rweb_video_timestamps_enabled": True,
            #     "longform_notetweets_rich_text_read_enabled": True,
            #     "longform_notetweets_inline_media_enabled": True,
            #     "responsive_web_media_download_video_enabled": False,
            #     "responsive_web_enhance_cards_enabled": False
            # } if func_name in [
#                 "allmedia", "images", "__tweetdetail"
#             ] else {
#                 "hidden_profile_likes_enabled": True,
#                 "hidden_profile_subscriptions_enabled": True,
#                 "responsive_web_graphql_exclude_directive_enabled": True,
#                 "verified_phone_label_enabled": False,
#                 "subscriptions_verification_info_is_identity_verified_enabled": True,
#                 "subscriptions_verification_info_verified_since_enabled": True,
#                 "highlights_tweets_tab_ui_enabled": True,
#                 "responsive_web_twitter_article_notes_tab_enabled": False,
#                 "creator_subscriptions_tweet_preview_api_enabled": True,
#                 "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
#                 "responsive_web_graphql_timeline_navigation_enabled": True
#             }
#         }

#         if func_name in ["get_rest_id", "__tweetdetail"]:
#             payload.update({"fieldToggles": fieldToggles})
#         return payload