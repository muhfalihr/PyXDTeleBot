import io
import os
import re
import json
import telebot
import logging
import inspect
import hashlib

from requests.sessions import Session
from telebot import types
from urllib.parse import quote
from PyXDBot.exception import *
from PyXDBot.logger import setup_logging
from faker import Faker
from typing import Any, Optional
from dotenv import load_dotenv


class PyXDTelebot:
    def __init__(self) -> Any:
        load_dotenv()

        TOKEN = os.environ.get("TELEBOT_TOKEN")
        self.__bot = telebot.TeleBot(token=TOKEN)

        self.__cookie = os.environ.get("X_COOKIE")
        self.__session = Session()
        self.__fake = Faker()

        setup_logging()
        self.__logger = logging.getLogger(self.__class__.__name__)

        self.__headers = dict()
        self.__headers["Accept"] = "application/json, text/plain, */*"
        self.__headers["Accept-Language"] = "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
        self.__headers["Sec-Fetch-Dest"] = "empty"
        self.__headers["Sec-Fetch-Mode"] = "cors"
        self.__headers["Sec-Fetch-Site"] = "same-site"
        self.__headers["Authorization"] = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
        self.__headers["Cookie"] = self.__cookie

        self.__http_error_status_code = None
        self.__http_error_reason = None

        self.__current_func = lambda: inspect.getouterframes(
            inspect.currentframe()
        )[1][3]
        self.__convertws = lambda data_dict: re.sub(
            r'\s+', '', json.dumps(data_dict))
        self.__hashmd5 = lambda url: hashlib.md5().update(url.encode("utf-8")).hexdigest()

        @self.__bot.message_handler(commands=["start", "hello"])
        def instruction(message):
            id = message.chat.id
            username = message.from_user.username

            self.__bot.reply_to(
                message=message,
                text=f"Welcome👋, {username}"
            )
            self.__bot.send_message(
                chat_id=id,
                text=(
                    "Instructions for use:\n"
                    "  - /allmedia screen_name=screenname count=20 cursor=abcdefghij\n"
                    "  - /images screen_name=screenname count=20 cursor=abcdefghij\n"
                    "  - /linkdownloader https://x.com/screenname/status/postid?s=20\n\n"
                    "Explanation:\n"
                    "  - screen_name (Required)\n"
                    "  - count (Optional) Default = 20\n"
                    "  - cursor (Optional) Used to retrieve the next media.\n"
                )
            )

        @self.__bot.message_handler(commands=["allmedia", "am"])
        def send_allmedia(message):
            id = message.chat.id
            parameters = dict()

            for param in message.text.split():
                if "=" in param:
                    parameter = param.split("=")
                    parameters.update({parameter[0]: parameter[1]})

            if parameters:
                self.__bot.send_message(
                    chat_id=id,
                    text="Please Wait...."
                )

                try:
                    send_msg = self.__bot.send_message(
                        chat_id=id,
                        text="Loading"
                    )

                    medias, cursor_value = self.allmedia(**parameters)

                    media_group = []

                    for index, media in enumerate(medias):
                        self.__loading(
                            message=send_msg,
                            chat_id=id,
                            iterations=index
                        )

                        data, filename, content_type = self.__download(media)

                        databyte = io.BytesIO(data)
                        databyte.name = filename

                        if len(media_group) == 10:
                            media_group.clear()

                        if len(media_group) < 10:
                            if "image" in content_type:
                                media_group.append(
                                    types.InputMediaPhoto(media=databyte)
                                )
                            elif "video" in content_type:
                                media_group.append(
                                    types.InputMediaVideo(media=databyte)
                                )

                        if len(media_group) == 10:
                            self.__bot.send_media_group(
                                chat_id=id,
                                media=media_group
                            )

                    if media_group:
                        self.__bot.send_media_group(
                            chat_id=id,
                            media=media_group
                        )

                    if cursor_value:
                        self.__bot.send_message(
                            chat_id=id, text=f"Cursor Value for next media = {cursor_value}")
                    else:
                        self.__bot.send_message(
                            chat_id=id, text="Done 😊")

                except Exception:
                    self.__bot.send_message(
                        chat_id=id,
                        text=f"Error! status code {self.__http_error_status_code} : {self.__http_error_reason}"
                    )

            else:
                self.__bot.send_message(
                    chat_id=id, text=f"Your command is not correct.")
                self.__bot.send_message(
                    chat_id=id,
                    text=(
                        "Instructions for use:\n"
                        "  - /allmedia screen_name=screenname count=20 cursor=abcdefghij\n"
                        "  - /images screen_name=screenname count=20 cursor=abcdefghij\n"
                        "  - /linkdownloader https://x.com/screenname/status/postid?s=20\n\n"
                        "Explanation:\n"
                        "  - screen_name (Required)\n"
                        "  - count (Optional) Default = 20\n"
                        "  - cursor (Optional) Used to retrieve the next media.\n"
                    )
                )

        @self.__bot.message_handler(commands=["images", "imgs"])
        def send_images(message):
            id = message.chat.id
            parameters = dict()

            for param in message.text.split():
                if "=" in param:
                    parameter = param.split("=")
                    parameters.update({parameter[0]: parameter[1]})

            if parameters:
                self.__bot.send_message(
                    chat_id=id,
                    text="Please Wait...."
                )

                try:
                    send_msg = self.__bot.send_message(
                        chat_id=id,
                        text="Loading"
                    )

                    medias, cursor_value = self.images(**parameters)

                    media_group = []

                    for index, media in enumerate(medias):
                        self.__loading(
                            message=send_msg,
                            chat_id=id,
                            iterations=index
                        )

                        data, filename, content_type = self.__download(media)

                        databyte = io.BytesIO(data)
                        databyte.name = filename

                        if len(media_group) == 10:
                            media_group.clear()

                        if len(media_group) < 10:
                            media_group.append(
                                types.InputMediaPhoto(media=databyte)
                            )

                        if len(media_group) == 10:
                            self.__bot.send_media_group(
                                chat_id=id,
                                media=media_group
                            )

                    if media_group:
                        self.__bot.send_media_group(
                            chat_id=id,
                            media=media_group
                        )

                    if cursor_value:
                        self.__bot.send_message(
                            chat_id=id, text=f"Cursor Value for next media = {cursor_value}")
                    else:
                        self.__bot.send_message(
                            chat_id=id, text="Done 😊")

                except Exception:
                    self.__bot.send_message(
                        chat_id=id,
                        text=f"Error! status code {self.__http_error_status_code} : {self.__http_error_reason}"
                    )

            else:
                self.__bot.send_message(
                    chat_id=id, text=f"Your command is not correct.")
                self.__bot.send_message(
                    chat_id=id,
                    text=(
                        "Instructions for use:\n"
                        "  - /allmedia screen_name=screenname count=20 cursor=abcdefghij\n"
                        "  - /images screen_name=screenname count=20 cursor=abcdefghij\n"
                        "  - /linkdownloader https://x.com/screenname/status/postid?s=20\n\n"
                        "Explanation:\n"
                        "  - screen_name (Required)\n"
                        "  - count (Optional) Default = 20\n"
                        "  - cursor (Optional) Used to retrieve the next media.\n"
                    )
                )

        @self.__bot.message_handler(commands=["linkdownloader", "ld"])
        def send_media_from_ld(message):
            id = message.chat.id
            param = ""

            pattern = r'https://x\.com/[\w_]+/status/\d+\?s=20'

            try:
                param = message.text.split()[1]

                if re.match(pattern=pattern, string=param):
                    send_msg = self.__bot.send_message(
                        chat_id=id,
                        text="Please Wait...."
                    )

                    try:
                        medias = self.linkdownloader(param)

                        media_group = []

                        for i, media in enumerate(medias):
                            if len(medias) > 1:
                                self.__loading(
                                    message=send_msg,
                                    chat_id=id,
                                    iterations=i
                                )

                            data, filename, content_type = self.__download(
                                media
                            )

                            databyte = io.BytesIO(data)
                            databyte.name = filename

                            if len(media_group) == 10:
                                media_group.clear()

                            if len(media_group) < 10:
                                if "image" in content_type:
                                    media_group.append(
                                        types.InputMediaPhoto(media=databyte)
                                    )
                                elif "video" in content_type:
                                    media_group.append(
                                        types.InputMediaVideo(media=databyte)
                                    )

                            if len(media_group) == 10:
                                self.__bot.send_media_group(
                                    chat_id=id,
                                    media=media_group
                                )

                        if media_group:
                            self.__bot.send_media_group(
                                chat_id=id,
                                media=media_group
                            )

                        self.__bot.send_message(
                            chat_id=id, text="Media download is complete.")

                    except Exception:
                        self.__bot.send_message(
                            chat_id=id,
                            text=f"Error! status code {self.__http_error_status_code} : {self.__http_error_reason}"
                        )

                else:
                    self.__bot.send_message(
                        chat_id=id, text=f"Your command is not correct.")
                    self.__bot.send_message(
                        chat_id=id,
                        text=(
                            "Instructions for use:\n"
                            "  - /allmedia screen_name=screenname count=20 cursor=abcdefghij\n"
                            "  - /images screen_name=screenname count=20 cursor=abcdefghij\n"
                            "  - /linkdownloader https://x.com/screenname/status/postid?s=20\n\n"
                            "Explanation:\n"
                            "  - screen_name (Required)\n"
                            "  - count (Optional) Default = 20\n"
                            "  - cursor (Optional) Used to retrieve the next media.\n"
                        )
                    )

            except IndexError:
                self.__bot.send_message(
                    chat_id=id, text=f"Your command is not correct.")
                self.__bot.send_message(
                    chat_id=id,
                    text=(
                        "Instructions for use:\n"
                        "  - /allmedia screen_name=screenname count=20 cursor=abcdefghij\n"
                        "  - /images screen_name=screenname count=20 cursor=abcdefghij\n"
                        "  - /linkdownloader https://x.com/screenname/status/postid?s=20\n\n"
                        "Explanation:\n"
                        "  - screen_name (Required)\n"
                        "  - count (Optional) Default = 20\n"
                        "  - cursor (Optional) Used to retrieve the next media.\n"
                    )
                )

    def __loading(self, message: str, chat_id: int | str, iterations: int):
        loading_text = f"Loading {'⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'[iterations % 10]}"

        self.__bot.edit_message_text(
            chat_id=chat_id,
            message_id=message.message_id,
            text=loading_text
        )

    def __csrftoken(self) -> str:
        self.__logger.info("Retrieves X-Csrf-Token from cookie.")

        pattern = re.compile(r'ct0=([a-zA-Z0-9_-]+)')
        matches = pattern.search(self.__cookie)
        if matches:
            csrftoken = matches.group(1)
            return csrftoken
        else:
            self.__logger.error(
                CSRFTokenMissingError(
                    "Error! CSRF token is missing. Please ensure that a valid CSRF token is included in the cookie."
                )
            )

    def __buildpayload(self, **kwargs) -> dict:
        self.__logger.info("Building payloads")

        func_name = kwargs["func_name"]
        match func_name:
            case "__profile":
                screen_name = kwargs["screen_name"]

                variables = {
                    "screen_name": screen_name.lower(),
                    "withSafetyModeUserFields": True
                }

                fieldToggles = {"withAuxiliaryUserLabels": False}

            case "__tweetdetail":
                focalTweetId = kwargs["focalTweetId"]
                controller_data = kwargs["controller_data"]
                cursor = kwargs["cursor"]

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

                fieldToggles = {"withArticleRichContentState": False}

            case "allmedia" | "images":
                userId = kwargs["userId"]
                count = kwargs["count"]
                cursor = kwargs["cursor"]

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

        payload = {
            "variables": variables,
            "features": {
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
            } if func_name in [
                "allmedia", "images", "__tweetdetail"
            ] else {
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
        }
        if func_name in ["__profile", "__tweetdetail"]:
            payload.update(
                {
                    "fieldToggles": fieldToggles
                }
            )

        return payload

    def __profile(self, screen_name: str, proxy: Optional[str] = None, **kwargs) -> dict:
        user_agent = self.__fake.user_agent()
        function_name = self.__current_func()

        self.__logger.info(
            f"Carry out the rest_id retrieval process in the {function_name} function."
        )

        payload = self.__buildpayload(
            func_name=function_name,
            screen_name=screen_name
        )
        for key in payload:
            payload.update({key: self.__convertws(payload[key])})

        variables = quote(payload["variables"])
        features = quote(payload["features"])
        fieldToggles = quote(payload["fieldToggles"])

        url = "https://api.twitter.com/graphql/NimuplG1OB7Fd2btCLdBOw/UserByScreenName?variables={variables}&features={features}&fieldToggles={fieldToggles}".format(
            variables=variables,
            features=features,
            fieldToggles=fieldToggles
        )

        self.__headers["User-Agent"] = user_agent
        self.__headers["X-Csrf-Token"] = self.__csrftoken()

        self.__logger.info(
            "Process requests to Twitter User Profiles using the GET method."
        )

        resp = self.__session.request(
            method="GET",
            url=url,
            timeout=60,
            proxies=proxy,
            headers=self.__headers,
            **kwargs
        )
        status_code = resp.status_code
        content = resp.content
        if status_code == 200:
            response = content.decode('utf-8')
            data = json.loads(response)
            result = data["data"]["user"]["result"]
            rest_id = result["rest_id"]

            self.__logger.info("rest_id successfully obtained.")

            return rest_id
        else:
            self.__logger.error(
                HTTPErrorException(
                    f"Error! status code {resp.status_code} : {resp.reason}"
                )
            )

    def __download(self, url: str) -> Any:
        self.__logger.info(
            f"Carry out the process to retrieve content, filename, and content_type in the {self.__current_func()} function."
        )

        user_agent = self.__fake.user_agent()
        self.__headers["User-Agent"] = user_agent

        self.__logger.info(
            "Make a request to the URL of the media from which the content will be retrieved using the GET method."
        )

        resp = self.__session.request(
            method="GET",
            url=url,
            headers=self.__headers,
            timeout=120
        )
        status_code = resp.status_code
        data = resp.content
        if status_code == 200:
            try:
                if ".mp4" in url:
                    pattern = re.compile(r'/([^/?]+)\?')
                    matches = pattern.search(url)
                    if matches:
                        filename = matches.group(1)
                    else:
                        filename = self.__hashmd5(url) + ".mp4"
                else:
                    filename = url.split("/")[-1]
            except IndexError:
                filename = self.__hashmd5(url) + ".jpg"
            content_type = resp.headers.get("Content-Type")

            self.__logger.info(
                "content, filename, and content type have been successfully obtained."
            )

            return data, filename, content_type
        else:
            self.__http_error_status_code = resp.status_code
            self.__http_error_reason = resp.reason

            self.__logger.error(
                HTTPErrorException(
                    f"Error! status code {resp.status_code} : {resp.reason}"
                )
            )

    def __processmedia(self, tweet_results: dict, func_name: str) -> list:
        self.__logger.info(
            f"Carry out the process of retrieving URLs from each media in the {self.__current_func()} function."
        )

        medias = []

        media_list = tweet_results.get("entities", {}).get("media", [])

        if media_list:
            for media in media_list:
                media_type = media.get("type", "")

                match func_name:
                    case "allmedia":
                        if media_type == "photo":
                            image = media.get("media_url_https", "")
                            medias.append(image)
                        if media_type == "video":
                            videos = max(media.get("video_info", {}).get(
                                "variants", []), key=lambda x: x.get("bitrate", 0)).get("url", "")
                            medias.append(videos)

                    case "images":
                        if media_type == "photo":
                            image = media.get("media_url_https", "")
                            medias.append(image)

                    case "__tweetdetail":
                        if media_type == "photo":
                            image = media.get("media_url_https", "")
                            medias.append(image)
                        elif media_type == "video":
                            videos = max(media.get("video_info", {}).get(
                                "variants", []), key=lambda x: x.get("bitrate", 0)).get("url", "")
                            medias.append(videos)

                self.__logger.info(
                    "The URL of each media has been successfully obtained."
                )
        else:
            quoted_status_id_str = tweet_results.get(
                "quoted_status_id_str", "")
            medias = self.__tweetdetail(focalTweetId=quoted_status_id_str)
            medias = medias if medias else []

        return medias

    def allmedia(self, **kwargs) -> dict:
        self.__logger.info(
            "Retrieves all media from photos and videos from specified Twitter user posts."
        )

        screen_name = kwargs.get("screen_name")
        count = kwargs.get("count", 20)
        cursor = kwargs.get("cursor", None)

        user_agent = self.__fake.user_agent()

        function_name = self.__current_func()
        userId = self.__profile(screen_name=screen_name)
        payload = self.__buildpayload(
            func_name=function_name,
            userId=userId,
            count=count,
            cursor=cursor
        )

        for key in payload:
            payload.update({key: self.__convertws(payload[key])})

        variables = quote(payload["variables"])
        features = quote(payload["features"])
        url = "https://twitter.com/i/api/graphql/oMVVrI5kt3kOpyHHTTKf5Q/UserMedia?variables={variables}&features={features}".format(
            variables=variables,
            features=features
        )
        self.__headers["User-Agent"] = user_agent
        self.__headers["X-Csrf-Token"] = self.__csrftoken()

        self.__logger.info(
            "Make a request to the URL UserMedia Twitter using the GET method."
        )

        resp = self.__session.request(
            method="GET",
            url=url,
            timeout=60,
            headers=self.__headers
        )
        status_code = resp.status_code
        content = resp.content
        if status_code == 200:
            response = content.decode('utf-8')
            data = json.loads(response)
            instructions = data["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"]

            medias = []
            for instruction in instructions:
                if isinstance(instruction, dict) and instruction["type"] == "TimelineAddEntries":

                    cursor_value = ""
                    for entry in instruction.get("entries", []):
                        content = entry.get("content", {})
                        item_content = content.get("itemContent", {})

                        tweet_results = item_content.get(
                            "tweet_results", {}
                        ).get(
                            "result", {}
                        ).get(
                            "legacy", {}
                        )

                        medias.extend(
                            self.__processmedia(
                                tweet_results=tweet_results,
                                func_name=function_name
                            )
                        )

                        items_content = content.get("items", {})

                        for item_content in items_content:
                            tweet_results = item_content.get(
                                "item", {}
                            ).get(
                                "itemContent", {}
                            ).get(
                                "tweet_results", {}
                            ).get(
                                "result", {}
                            ).get(
                                "legacy", {}
                            )

                            medias.extend(
                                self.__processmedia(
                                    tweet_results=tweet_results,
                                    func_name=function_name
                                )
                            )

                        cursor_value += content.get("value", "") if content.get(
                            "cursorType") == "Bottom" else ""

                if isinstance(instruction, dict) and instruction["type"] == "TimelineAddToModule":

                    for entry in instruction.get("moduleItems", []):
                        tweet_results = entry.get(
                            "item", {}
                        ).get(
                            "itemContent", {}
                        ).get(
                            "tweet_results", {}
                        ).get(
                            "result", {}
                        ).get(
                            "legacy", {}
                        )

                        medias.extend(
                            self.__processmedia(
                                tweet_results=tweet_results,
                                func_name=function_name
                            )
                        )
            self.__logger.info(
                "The process of retrieving all media and cursor values has been successful."
            )
            return medias, cursor_value
        else:
            self.__http_error_status_code = resp.status_code
            self.__http_error_reason = resp.reason

            self.__logger.error(
                HTTPErrorException(
                    f"Error! status code {resp.status_code} : {resp.reason}"
                )
            )

    def images(self, **kwargs) -> dict:
        self.__logger.info(
            "Retrieves images from the specified Twitter user's posts."
        )

        screen_name = kwargs.get("screen_name")
        cursor = kwargs.get("cursor", None)

        user_agent = self.__fake.user_agent()

        function_name = self.__current_func()
        userId = self.__profile(screen_name=screen_name)
        payload = self.__buildpayload(
            func_name=function_name,
            userId=userId,
            count=20,
            cursor=cursor
        )

        for key in payload:
            payload.update({key: self.__convertws(payload[key])})

        variables = quote(payload["variables"])
        features = quote(payload["features"])
        url = "https://twitter.com/i/api/graphql/oMVVrI5kt3kOpyHHTTKf5Q/UserMedia?variables={variables}&features={features}".format(
            variables=variables,
            features=features
        )
        self.__headers["User-Agent"] = user_agent
        self.__headers["X-Csrf-Token"] = self.__csrftoken()

        self.__logger.info(
            "Make a request to the URL Images Twitter using the GET method."
        )

        resp = self.__session.request(
            method="GET",
            url=url,
            timeout=60,
            headers=self.__headers,
        )
        status_code = resp.status_code
        content = resp.content
        if status_code == 200:
            response = content.decode('utf-8')
            data = json.loads(response)
            instructions = data["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"]

            medias = []
            for instruction in instructions:
                if isinstance(instruction, dict) and instruction["type"] == "TimelineAddEntries":
                    cursor_value = ""

                    for entry in instruction.get("entries", []):
                        content = entry.get("content", {})
                        item_content = content.get("itemContent", {})

                        tweet_results = item_content.get(
                            "tweet_results", {}
                        ).get(
                            "result", {}
                        ).get(
                            "legacy", {}
                        )

                        medias.extend(
                            self.__processmedia(
                                tweet_results=tweet_results,
                                func_name=function_name
                            )
                        )

                        items_content = content.get("items", {})

                        for item_content in items_content:
                            tweet_results = item_content.get(
                                "item", {}
                            ).get(
                                "itemContent", {}
                            ).get(
                                "tweet_results", {}
                            ).get(
                                "result", {}
                            ).get(
                                "legacy", {}
                            )

                            medias.extend(
                                self.__processmedia(
                                    tweet_results=tweet_results,
                                    func_name=function_name
                                )
                            )

                        cursor_value += content.get("value", "") if content.get(
                            "cursorType") == "Bottom" else ""

                if isinstance(instruction, dict) and instruction["type"] == "TimelineAddToModule":

                    for entry in instruction.get("moduleItems", []):
                        tweet_results = entry.get(
                            "item", {}
                        ).get(
                            "itemContent", {}
                        ).get(
                            "tweet_results", {}
                        ).get(
                            "result", {}
                        ).get(
                            "legacy", {}
                        )
                        medias.extend(
                            self.__processmedia(
                                tweet_results=tweet_results,
                                func_name=function_name
                            )
                        )

            self.__logger.info(
                "The process of retrieving images and cursor values has been successful."
            )
            return medias, cursor_value
        else:
            self.__http_error_status_code = resp.status_code
            self.__http_error_reason = resp.reason

            self.__logger.error(
                HTTPErrorException(
                    f"Error! status code {resp.status_code} : {resp.reason}"
                )
            )

    def __tweetdetail(
            self,
            focalTweetId: str | int,
            controller_data: Optional[str] = "DAACDAABDAABCgABAAAAAAAAAAAKAAkXK+YwNdoAAAAAAAA="
    ) -> list:
        self.__logger.info(
            "Retrieves media from the specified url of focalTweetId."
        )

        user_agent = self.__fake.user_agent()
        function_name = self.__current_func()
        payload = self.__buildpayload(
            func_name=function_name,
            focalTweetId=focalTweetId,
            controller_data=controller_data,
            cursor=None
        )
        for key in payload:
            payload.update({key: self.__convertws(payload[key])})

        variables = quote(payload["variables"])
        features = quote(payload["features"])
        fieldToggles = quote(payload["fieldToggles"])
        url = "https://twitter.com/i/api/graphql/-H4B_lJDEA-O_7_qWaRiyg/TweetDetail?variables={variables}&features={features}&fieldToggles={fieldToggles}".format(
            variables=variables,
            features=features,
            fieldToggles=fieldToggles
        )
        self.__headers["User-Agent"] = user_agent
        self.__headers["X-Csrf-Token"] = self.__csrftoken()

        self.__logger.info(
            "Make a request to the URL TweetDetail User Post using the GET method."
        )

        resp = self.__session.request(
            method="GET",
            url=url,
            timeout=60,
            headers=self.__headers
        )
        status_code = resp.status_code
        content = resp.content
        if status_code == 200:
            response = content.decode('utf-8')
            data = json.loads(response)
            instructions = data["data"]["threaded_conversation_with_injections_v2"]["instructions"]
            medias = []

            for instruction in instructions:
                if isinstance(instruction, dict) and instruction["type"] == "TimelineAddEntries":
                    for entry in instruction.get("entries", []):
                        content = entry.get("content", {})
                        item_content = content.get("itemContent", {})

                        tweet_results = item_content.get(
                            "tweet_results", {}
                        ).get(
                            "result", {}
                        ).get(
                            "legacy", {}
                        )

                        medias.extend(
                            self.__processmedia(
                                tweet_results=tweet_results,
                                func_name=function_name
                            )
                        )

            self.__logger.info(
                "The process of retrieving media has been successful."
            )
            return medias
        else:
            self.__http_error_status_code = resp.status_code
            self.__http_error_reason = resp.reason

            self.__logger.error(
                HTTPErrorException(
                    f"Error! status code {resp.status_code} : {resp.reason}"
                )
            )

    def linkdownloader(self, link: str) -> Any:
        self.__logger.info(
            "Carry out the process of retrieving the focalTweetId from the link provided in the message."
        )

        pattern = re.compile(r'/([^/?]+)\?')
        matches = pattern.search(string=link)
        if matches:
            focalTweetId = matches.group(1)
        else:
            self.__logger.error(
                URLValidationError(
                    f"Error! Invalid URL \"{link}\". Make sure the URL is correctly formatted and complete."
                )
            )

        medias = self.__tweetdetail(focalTweetId=focalTweetId)
        return medias

    def start_polling(self):
        self.__logger.info("Starting the PyXDTelebot program has gone well.")
        self.__bot.polling(non_stop=True)


if __name__ == "__main__":
    sb = PyXDTelebot()
