import re
import json
import logging

from functools import wraps
from PyXDBot.process import Process
from typing import Any, Dict, List, ByteString
from PyXDBot.exception import *
from PyXDBot.logger import setup_logging

class Proccessor:
    def __init__(self) -> None:
        '''
        The core process of retrieving Media URLs and other important processes.

        ---
        '''
    @staticmethod
    def csrftoken(cookie: str) -> str:
        """
        Retrieves X-Csrf-Token from cookie
        """
        pattern = re.compile(r'ct0=([a-zA-Z0-9_-]+)')
        matches = pattern.search(cookie)
        if matches:
            csrftoken = matches.group(1)
            return csrftoken
        else:
            ...
    
    @staticmethod
    def payload(func):
        """
        builder payload
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            raw_payloads = func(*args, **kwargs)

            payload: Dict[str] = {"variables": raw_payloads[0], "features": raw_payloads[1]}
            try:
                payload.update({"fieldToggles": raw_payloads[2]})
            except Exception: pass
            return payload
        return wrapper
    
    @staticmethod
    def rest_id_getter(func):
        """
        rest_id getter
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            content = func(*args, **kwargs)

            data: Dict[Any] = json.loads(content.decode("utf-8"))
            result: Dict[Any] = data["data"]["user"]["result"]
            return result.get("rest_id")
        return wrapper
    
    @staticmethod
    def media_getter(func):
        """
        url media getter
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            content, features = func(*args, **kwargs)

            data: Dict[str] = json.loads(content.decode("utf-8"))
            medias: List[str] = []
            cursor_value: str = ""
            
            if features != "tweetdetail":
                instructions: List[dict] = data["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"]
                    
                for ins in instructions:
                    if isinstance(ins, dict) and ins["type"] == "TimelineAddEntries":

                        for entry in ins.get("entries", []):
                            item_content: Dict[dict] = entry.get("content", {}).get("itemContent", {})
                            tweet_results: Dict[dict] = item_content.get("tweet_results", {}).get("result", {}).get("legacy", {})
                            medias.extend(Process.processmedia(tweet_results=tweet_results,feature=features))

                            items_content: Dict[dict] = entry.get("content", {}).get("items", {})

                            for ic in items_content:
                                tweet_results: Dict[dict] = ic.get("item", {}).get("itemContent", {}).get("tweet_results", {}).get("result", {}).get("legacy", {})
                                medias.extend(Process.processmedia(tweet_results=tweet_results,feature=features))

                            cursor_value += entry.get("content", {}).get("value", "") if entry.get("content", {}).get("cursorType") == "Bottom" else ""

                    if isinstance(ins, dict) and ins["type"] == "TimelineAddToModule":

                        for entry in ins.get("moduleItems", []):
                            tweet_results: Dict[dict] = entry.get("item", {}).get("itemContent", {}).get("tweet_results", {}).get("result", {}).get("legacy", {})

                            medias.extend(Process.processmedia(tweet_results=tweet_results,feature=features))
            else:
                instructions: List[dict] = data["data"]["threaded_conversation_with_injections_v2"]["instructions"]

                for instruction in instructions:
                    if isinstance(instruction, dict) and instruction["type"] == "TimelineAddEntries":
                        
                        for entry in instruction.get("entries", []):
                            content: Dict[dict] = entry.get("content", {})
                            item_content: Dict[dict] = content.get("itemContent", {})
                            tweet_results: Dict[dict] = item_content.get("tweet_results", {}).get("result", {}).get("legacy", {})
                            quoted_status_result: Dict[dict] = item_content.get("tweet_results", {}).get("result", {}).get("quoted_status_result", {})

                            if quoted_status_result:
                                result: Dict[dict] = quoted_status_result.get("result", {}).get("legacy", {})
                                medias.extend(Process.processmedia(tweet_results=result, feature=features))
                            else:
                                medias.extend(Process.processmedia(tweet_results=tweet_results,feature=features))
            
            return medias, cursor_value
        return wrapper