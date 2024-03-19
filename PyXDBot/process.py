from typing import List, Dict, Any

class Process:
    def __init__(self) -> None:
        '''
        Media URL Retrieval Processor in the form of Images or Videos.

        :mod:`processmedia function` : Retrieve the image or video media URL with the best quality.
        '''

    @staticmethod
    def processmedia(tweet_results: Dict[dict, any], feature: str) -> List[str]:
        '''
        Retrieve the image or video media URL with the best quality.

        Arguments :
          - :mod:`tweet_results` (Dict[str, dict]) : Tweet results containing media information.
          - :mod:`feature` (str) : The feature to process media for.
        '''
        medias: List[str] = []

        media_list: List[str, any] = tweet_results.get("entities", {}).get("media", [])

        if media_list:
            for media in media_list:
                media_type: str = media.get("type", "")

                match feature:
                    case "allmedia":
                        if media_type == "photo":
                            image: str = media.get("media_url_https", "")
                            medias.append(image)
                        if media_type == "video":
                            videos: str = max(media.get("video_info", {}).get("variants", []), key=lambda x: x.get("bitrate", 0)).get("url", "")
                            medias.append(videos)

                    case "images":
                        if media_type == "photo":
                            image: str = media.get("media_url_https", "")
                            medias.append(image)
                    
                    case "videos":
                        if media_type == "video":
                            videos: str = max(media.get("video_info", {}).get("variants", []), key=lambda x: x.get("bitrate", 0)).get("url", "")
                            medias.append(videos)

                    case "tweetdetail":
                        if media_type == "photo":
                            image: str = media.get("media_url_https", "")
                            medias.append(image)
                        if media_type == "video":
                            videos: str = max(media.get("video_info", {}).get("variants", []), key=lambda x: x.get("bitrate", 0)).get("url", "")
                            medias.append(videos)
        return medias