import io
import os
import re
import json
import logging
import inspect
import hashlib

from requests.sessions import Session
from telebot import types, async_telebot
from urllib.parse import quote
# from PyXDBot.exception import *
# from PyXDBot.logger import setup_logging

from exception import *
from logger import setup_logging
from utility import Proccessor
from payload import BuilderPayloads

from faker import Faker
from typing import Any, Optional
from dotenv import load_dotenv



class PyXDTelebot:
    def __init__(self) -> Any:
        load_dotenv()

        TOKEN = os.environ.get("TELEBOT_TOKEN")
        self.__bot = async_telebot.AsyncTeleBot(token=TOKEN)

        self.__cookie = os.environ.get("X_COOKIE")
        self.__session = Session()
        self.__fake = Faker()

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

        self.__buildpayload = BuilderPayloads()
        self.__current_func = lambda: inspect.getouterframes(inspect.currentframe())[1][3]
        self.__delws = lambda text: re.sub(r'\s', '', text)
        self.__hashmd5 = lambda url: hashlib.md5().update(url.encode("utf-8")).hexdigest()

        setup_logging()
        self.__logger = logging.getLogger(self.__class__.__name__)

        

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
    
    @Proccessor.rest_id_getter
    def __get_rest_id(self, **kwargs):
        self.__logger.info(f"Carry out the rest_id retrieval process in the {self.__current_func()} function.")

        user_agent = self.__fake.user_agent()
        payload = self.__buildpayload.payload_UserByScreenName(**kwargs)

        for key in payload: payload.update({key: self.__delws(json.dumps(payload[key]))})

        payload_fragment = quote(payload["variables"]), quote(payload["features"]), quote(payload["fieldToggles"])

        url = f"https://api.twitter.com/graphql/NimuplG1OB7Fd2btCLdBOw/UserByScreenName?variables={payload_fragment[0]}&features={payload_fragment[1]}&fieldToggles={payload_fragment[2]}"

        self.__headers["User-Agent"] = user_agent
        self.__headers["X-Csrf-Token"] = self.__csrftoken()

        self.__logger.info("Process requests to Twitter User Profiles using the GET method.")

        resp = self.__session.request(
            method="GET",
            url=url,
            timeout=240,
            headers=self.__headers
        )
        status_code = resp.status_code
        content = resp.content
        
        if status_code == 200: return content
        else: self.__logger.error(HTTPErrorException(f"Error! status code {resp.status_code} : {resp.reason}"))

    @Proccessor.media_getter
    def __media_url_getter(self, **kwargs):
        self.__logger.info("Retrieves all media from photos and videos from specified Twitter user posts.")

        user_agent = self.__fake.user_agent()
        userId = self.__get_rest_id(**kwargs)
        payload = self.__buildpayload.payload_UserMedia(userId=userId, **kwargs)

        for key in payload: payload.update({key: self.__delws(json.dumps(payload[key]))})

        payload_fragment = quote(payload["variables"]), quote(payload["features"])

        url = f"https://twitter.com/i/api/graphql/oMVVrI5kt3kOpyHHTTKf5Q/UserMedia?variables={payload_fragment[0]}&features={payload_fragment[1]}"

        self.__headers["User-Agent"] = user_agent
        self.__headers["X-Csrf-Token"] = self.__csrftoken()

        self.__logger.info("Make a request to the URL UserMedia Twitter using the GET method.")

        resp = self.__session.request(
            method="GET",
            url=url,
            timeout=240,
            headers=self.__headers
        )
        status_code = resp.status_code
        content = resp.content
        features = kwargs.get("features")
        if status_code == 200: return content, features
        else: self.__logger.error(HTTPErrorException(f"Error! status code {resp.status_code} : {resp.reason}"))

    @Proccessor.media_getter
    def media_tweet_detail(self, **kwargs):
        self.__logger.info("Retrieves media from the specified url of focalTweetId.")

        user_agent = self.__fake.user_agent()
        payload = self.__buildpayload.payload_TweetDetail(**kwargs)

        for key in payload: payload.update({key: self.__delws(json.dumps(payload[key]))})

        payload_fragment = quote(payload["variables"]), quote(payload["features"]), quote(payload["fieldToggles"])

        url = f"https://twitter.com/i/api/graphql/89OGj-X6Vddr9EbuwIEmgg/TweetDetail?variables={payload_fragment[0]}&features={payload_fragment[1]}&fieldToggles={payload_fragment[2]}"

        self.__headers["User-Agent"] = user_agent
        self.__headers["X-Csrf-Token"] = self.__csrftoken()

        self.__logger.info("Make a request to the URL TweetDetail User Post using the GET method.")

        resp = self.__session.request(
            method="GET",
            url=url,
            timeout=60,
            headers=self.__headers
        )
        status_code = resp.status_code
        content = resp.content
        features = "tweetdetail"
        if status_code == 200: return content, features
        else: self.__logger.error(HTTPErrorException(f"Error! status code {resp.status_code} : {resp.reason}"))

if __name__ == "__main__":
    sb = PyXDTelebot()
    cek = sb.media_tweet_detail(focalTweetId="1744344182787821882")
    # print(cek)