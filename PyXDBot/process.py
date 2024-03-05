
class Process:

    @staticmethod
    def processmedia(tweet_results: list, feature: str):
        medias: list = []

        media_list: list = tweet_results.get("entities", {}).get("media", [])

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

        # else:
        #     quoted_status_id_str = tweet_results.get(
        #         "quoted_status_id_str", "")
        #     medias = self.__tweetdetail(focalTweetId=quoted_status_id_str)
        #     medias = medias if medias else []

        return medias