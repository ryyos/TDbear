import requests
import os

from tqdm import tqdm
from urllib import request
from dotenv import *
from uuid import uuid4
from icecream import ic
from datetime import datetime
from typing import Generator
from time import time

from src.exceptions.ExpiredExceptions import ExpiredExceptions

class Instagram:
    def __init__(self) -> {}:
        load_dotenv()

        self.__COOKIES = os.getenv('COOKIES')
        self.__IG_CLAIM = os.getenv('IG_CLAIM')
        self.__PATH_TO_SAVE = os.getenv('PATH_TO_SAVE')

        self.__USER_ID_API = 'https://www.instagram.com/web/search/topsearch/?query='



    def __build_header(self, username: str) -> dict:

        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cookie': self.__COOKIES,
            'Dpr': '1',
            'Referer': f'https://www.instagram.com/{username}/',
            'Sec-Ch-Prefers-Color-Scheme': 'dark',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Full-Version-List': '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.130", "Google Chrome";v="120.0.6099.130"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Model': '""',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Ch-Ua-Platform-Version': '"15.0.0"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Viewport-Width': '1920',
            'X-Asbd-Id': '129477',
            'X-Csrftoken': 'VqFUdHhunrwbNuPNn3UgjYlWYMPHrnwD',
            'X-Ig-App-Id': '936619743392459',
            'X-Ig-Www-Claim': self.__IG_CLAIM,
            'X-Requested-With': 'XMLHttpRequest'
        }

        return headers


    def __curl(self, path: str, url: str):
        try:
            if url: request.urlretrieve(url, path)
        except Exception as err:
            ic(err)
        

    def extract_data(self, document: dict) -> dict:

        results = [
            {
                "taken_at": content.get("taken_at"),
                "id": content.get("id"),
                "commerciality_status": content.get("commerciality_status", None),
                "explore_hide_comments": content.get("explore_hide_comments", None),
                "is_quiet_post": content.get("is_quiet_post", None),
                "mezql_token": content.get("mezql_token", None),
                "tags": content.get("usertags", {}).get("in", [])[:1],
                "photo_of_you": content.get("photo_of_you", None),
                "has_liked": content.get("has_liked", None),
                "has_privately_liked": content.get("has_privately_liked", None),
                "like_count": content.get("like_count", None),
                "can_viewer_reshare": content.get("can_viewer_reshare", None),
                "video_subtitles": content.get("video_subtitles_uri", None),
                "captions": content.get("caption", {}).get("text") if content.get("caption") is not None else None,
                "play_count": content.get("play_count", None),
                "medias": {
                    "carousel_media": [medias.get("image_versions2", {}).get("candidates", None) for medias in content.get("carousel_media", {})],
                    "carousel_video": [medias["video_versions"] for medias in content.get("carousel_media", {}) if medias.get("video_versions")],
                    "images": content.get("image_versions2", {}).get("candidates", None),
                    "videos": content.get("video_versions", None),
                    "video_durations": content.get("video_duration", None)
                }
                    
            } for content in document["items"]
        ]
        
        return results

    def check(format: str) -> bool:
        if format == 'image' or format == 'all': return 

    def main(self, username: str, format: str):

        response = requests.get(url=f'https://www.instagram.com/api/v1/feed/user/{username}/username/?count=12', headers=self.__build_header(username=username))
        user_id = requests.get(url=self.__USER_ID_API+username, headers=self.__build_header(username=username))
        
        user_id = user_id.json()['users'][0]['user']['pk_id']
        if response.status_code != 200: raise ExpiredExceptions('your COOKIES or IG CLAIM is Expired, Update Please!')

        # if not os.path.exists(f'{self.__PATH_TO_SAVE}/{username}'):
        #     os.mkdir(f'{self.__PATH_TO_SAVE}/{username}')
        #     os.mkdir(f'{self.__PATH_TO_SAVE}/{username}/{username}_images')
        #     os.mkdir(f'{self.__PATH_TO_SAVE}/{username}/{username}_videos')
        #     os.mkdir(f'{self.__PATH_TO_SAVE}/{username}/json')

        
        response = response.json()

        results = {
                "crawling_time": str(datetime.now()),
                "crawling_time_epoch": int(time()),
                "search_key": username,
                "status": response["status"],
                "user": {
                    "username": response["user"]["username"],
                    "full_name": response["user"]["full_name"],
                    "is_private": response["user"]["is_private"],
                    "is_verified": response["user"]["is_verified"],
                    "profile_pic_id": response["user"]["profile_pic_id"],
                    "profile_pic_url": response["user"]["profile_pic_url"],
                },
                "contents":[]
            }

        next_max_id = response.get("next_max_id", None)
        while True:

            contents = self.extract_data(document=response)

            # results["contents"].append(contents)

            for content in tqdm(contents, ascii=True, smoothing=0.1, total=len(contents)):

                if bool(content["medias"]["videos"]) and (format == 'video' or format == 'all'):
                    # self.__curl(
                    #     url=content["medias"]["videos"][0]["url"],
                    #     path=f"{self.__PATH_TO_SAVE}/{username}/{username}_videos/{str(round(time() * 1000))}.mp4"
                    #     )

                    yield content["medias"]["videos"][0]["url"]

                if content["medias"]["carousel_media"] or content["medias"]["carousel_video"]:

                    if format == 'image' or format == 'all': 
                        for medias in content["medias"]["carousel_media"]:
                            max_resolution = max(medias, key=lambda x: x['width'] * x['height'] if x['width'] != x['height'] else 0)
                            yield max_resolution["url"]+'#inifoto'


                    if format == 'video' or format == 'all': 
                        for videos in content["medias"]["carousel_video"]:
                            max_resolution = max(videos, key=lambda x: x['width'] * x['height'])
                            yield max_resolution["url"]
                        
            

            if not next_max_id: break

            response = requests.get(url=f'https://www.instagram.com/api/v1/feed/user/{user_id}/?count=12&max_id={next_max_id}', headers=self.__build_header(username=username))
            ic(response)
            response = response.json()

            next_max_id = response.get("next_max_id", None)
            


        # self.__file.write_json(path=f'{self.__PATH_TO_SAVE}/{username}/json/{username}.json', content=results)
        