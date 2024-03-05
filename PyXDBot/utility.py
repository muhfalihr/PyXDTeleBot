import json

from functools import wraps
from process import Process

class Proccessor:

    @staticmethod
    def payload(func):
        """
        builder payload
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            raw_payloads = func(*args, **kwargs)

            payload = {"variables": raw_payloads[0], "features": raw_payloads[1]}
            try: payload.update({"fieldToggles": raw_payloads[2]})
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

            data = json.loads(content.decode("utf-8"))
            result = data["data"]["user"]["result"]
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

            data = json.loads(content.decode("utf-8"))
            medias = []
            cursor_value = ""
            
            if features != "tweetdetail":
                instructions = data["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"]
                    
                for ins in instructions:
                    if isinstance(ins, dict) and ins["type"] == "TimelineAddEntries":

                        for entry in ins.get("entries", []):
                            item_content = entry.get("content", {}).get("itemContent", {})
                            tweet_results = item_content.get("tweet_results", {}).get("result", {}).get("legacy", {})
                            medias.extend(Process.processmedia(tweet_results=tweet_results,feature=features))

                            items_content = entry.get("content", {}).get("items", {})

                            for ic in items_content:
                                tweet_results = ic.get("item", {}).get("itemContent", {}).get("tweet_results", {}).get("result", {}).get("legacy", {})
                                medias.extend(Process.processmedia(tweet_results=tweet_results,feature=features))

                            cursor_value += entry.get("content", {}).get("value", "") if entry.get("content", {}).get("cursorType") == "Bottom" else ""

                    if isinstance(ins, dict) and ins["type"] == "TimelineAddToModule":

                        for entry in ins.get("moduleItems", []):
                            tweet_results = entry.get("item", {}).get("itemContent", {}).get("tweet_results", {}).get("result", {}).get("legacy", {})

                            medias.extend(Process.processmedia(tweet_results=tweet_results,feature=features))
            else:
                instructions = data["data"]["threaded_conversation_with_injections_v2"]["instructions"]

                for instruction in instructions:
                    if isinstance(instruction, dict) and instruction["type"] == "TimelineAddEntries":
                        for entry in instruction.get("entries", []):
                            content = entry.get("content", {})
                            item_content = content.get("itemContent", {})
                            tweet_results = item_content.get("tweet_results", {}).get("result", {}).get("legacy", {})
                            quoted_status_result = item_content.get("tweet_results", {}).get("result", {}).get("quoted_status_result", {})

                            if quoted_status_result:
                                result = quoted_status_result.get("result", {}).get("legacy", {})
                                medias.extend(Process.processmedia(tweet_results=result, feature=features))
                            else:
                                medias.extend(Process.processmedia(tweet_results=tweet_results,feature=features))
            
            return medias, cursor_value
            # result = {"medias": medias}
            # dumps = json.dumps(result, indent=4)
            # with open("result.json", "w") as file:
            #     file.write(dumps)
        return wrapper