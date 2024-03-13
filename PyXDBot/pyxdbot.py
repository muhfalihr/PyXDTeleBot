import io
import os
import re
import json
import logging
import inspect
import hashlib
import asyncio

from PyXDBot.exception import *
from PyXDBot.logger import setup_logging
from PyXDBot.utility import Proccessor
from PyXDBot.payload import BuilderPayloads

from datetime import datetime
from requests.sessions import Session
from telebot import types, async_telebot
from urllib.parse import quote
from faker import Faker
from typing import Any, List, Tuple
from dotenv import load_dotenv


class PyXDTelebot:
    def __init__(self) -> Any:
        '''
        PyXDTelebot is a Telegram bot created using the Python programming language,
        specifically designed to facilitate the seamless sharing of media such as photos and videos from Twitter user posts.
        The bot leverages the Twitter API to extract multimedia content from a user's post and swiftly deliver it automatically to users through the Telegram platform.
        '''
        load_dotenv()

        self.cookie = os.environ.get("X_COOKIE")
        self.session = Session()
        self.fake = Faker()

        self.headers = dict()
        self.headers["Accept"] = "application/json, text/plain, */*"
        self.headers["Accept-Language"] = "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
        self.headers["Sec-Fetch-Dest"] = "empty"
        self.headers["Sec-Fetch-Mode"] = "cors"
        self.headers["Sec-Fetch-Site"] = "same-site"
        self.headers["Authorization"] = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
        self.headers["Cookie"] = self.cookie
        self.headers["User-Agent"] = self.fake.user_agent()
        self.headers["X-Csrf-Token"] = Proccessor.csrftoken(cookie=self.cookie)

        self.http_error_status_code = None
        self.http_error_reason = None

        self.buildpayload = BuilderPayloads()
        self.delws = lambda text: re.sub(r'\s', '', text)

        setup_logging()
        self.logger = logging.getLogger(self.__class__.__name__)

    @Proccessor.rest_id_getter
    def get_rest_id(self, **kwargs) -> str:
        '''
        Retrieve rest_id from Twitter UserByScreenName API

        Keyword Arguments :
          - **kwargs
        '''
        self.logger.info(f"Retrieve rest_id from Twitter UserByScreenName API")

        payload = self.buildpayload.payload_UserByScreenName(**kwargs)

        for key in payload: payload.update({key: self.delws(json.dumps(payload[key]))})

        payload_fragment = quote(payload["variables"]), quote(payload["features"]), quote(payload["fieldToggles"])

        url = f"https://api.twitter.com/graphql/NimuplG1OB7Fd2btCLdBOw/UserByScreenName?variables={payload_fragment[0]}&features={payload_fragment[1]}&fieldToggles={payload_fragment[2]}"

        self.logger.info("Make requests to the Twitter UserByScreenName API")

        resp = self.session.request(
            method="GET",
            url=url,
            timeout=480,
            headers=self.headers
        )
        status_code = resp.status_code
        content = resp.content

        self.logger.info(f"The request has been successfully carried out and received a response of {status_code}: {resp.reason}")
        
        if status_code == 200:
            return content
        else:
            self.http_error_status_code = resp.status_code
            self.http_error_reason = resp.reason
            self.logger.error(HTTPErrorException(f"Error! status code {resp.status_code} : {resp.reason}"))

    @Proccessor.media_getter
    def media_url_getter(self, **kwargs) -> List[str] | str:
        '''
        Taking media URLs in the form of images or videos with the following feature provisions All Media, Images, Videos, Link Downloader

        Keyword Arguments :
          - **kwargs
        '''
        self.logger.info(f"Taking media URLs in the form of images or videos with the following feature provisions: {kwargs.get('features')}")

        features = kwargs.get("features")

        if features != "tweetdetail":
            userId = self.get_rest_id(**kwargs)
            payload = self.buildpayload.payload_UserMedia(userId=userId, **kwargs)

            for key in payload: payload.update({key: self.delws(json.dumps(payload[key]))})

            payload_fragment = quote(payload["variables"]), quote(payload["features"])

            url = f"https://twitter.com/i/api/graphql/oMVVrI5kt3kOpyHHTTKf5Q/UserMedia?variables={payload_fragment[0]}&features={payload_fragment[1]}"
            
            self.logger.info("Make requests to the Twitter UserMedia API")
        
        else:
            payload = self.buildpayload.payload_TweetDetail(**kwargs)

            for key in payload: payload.update({key: self.delws(json.dumps(payload[key]))})

            payload_fragment = quote(payload["variables"]), quote(payload["features"]), quote(payload["fieldToggles"])

            url = f"https://twitter.com/i/api/graphql/89OGj-X6Vddr9EbuwIEmgg/TweetDetail?variables={payload_fragment[0]}&features={payload_fragment[1]}&fieldToggles={payload_fragment[2]}"

            self.logger.info("Make requests to the Twitter TweetDetail API")

        resp = self.session.request(
            method="GET",
            url=url,
            timeout=480,
            headers=self.headers
        )
        
        status_code = resp.status_code
        content = resp.content
        
        self.logger.info(f"The request has been successfully carried out and received a response of {status_code}: {resp.reason}")

        if status_code == 200:
            return content, features
        else:
            self.http_error_status_code = resp.status_code
            self.http_error_reason = resp.reason
            self.logger.error(HTTPErrorException(f"Error! status code {resp.status_code} : {resp.reason}"))
    
    @Proccessor.download
    def download(self, url: str) -> bytes | str:
        self.logger.info(f"Carry out the process to retrieve content, filename, and content_type in the download function.")
        self.logger.info("Make a request to the URL of the media from which the content will be retrieved using the GET method.")
        
        resp = self.session.request(
            method="GET",
            url=url,
            timeout=480,
            headers=self.headers
        )

        status_code = resp.status_code

        self.logger.info(f"The request has been successfully carried out and received a response of {status_code}: {resp.reason}")
        
        if status_code == 200:
            return resp, url
        else:
            self.http_error_status_code = resp.status_code
            self.http_error_reason = resp.reason

            self.logger.error(HTTPErrorException(f"Error! status code {resp.status_code} : {resp.reason}"))

if __name__ == "__main__":
    sb = PyXDTelebot()
