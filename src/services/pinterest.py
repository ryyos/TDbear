import requests
import os

from urllib.parse import urlencode
from requests import Response
from fake_useragent import FakeUserAgent
from datetime import datetime
from time import time, sleep
from ApiRetrys import ApiRetry
from icecream import ic
from json import dumps

class Pinterest:
    def __init__(self) -> None:
        self.__user_agent = FakeUserAgent()
        self.__retry = ApiRetry()
        self.__api = 'https://id.pinterest.com/resource/BaseSearchResource/get/'
        self.__base_url = "https://id.pinterest.com"

        self.__headers = {
            "User-Agent": self.__user_agent.random
        }


    def __create_param(self, query: str, size: int) -> dict:
        return {
            "options": {
                "article": "",
                "appliedProductFilters": "---",
                "price_max": "null",
                "price_min": "null",
                "scope": "pins",
                "auto_correction_disabled": "",
                "top_pin_id": "",
                "filters": "",
                "query": query,
                "page_size": size
            }
        }

    def __extract_data(self, resource: dict, query: str) -> dict:
        return {
            "domain": self.__api.split("/")[2],
            "crawling_time": datetime.now(),
            "crawling_time_epoch": int(time()),
            "query": query,
            "content": {
                "status": resource["status"],
                "message": resource["message"],
                "total": len(resource["data"]["results"]),
                "data": [
                    {
                        "url": f'{self.__base_url}/pin/{data["id"]}',
                        "description": data["description"],
                        "author": {
                            "name": data["pinner"]["full_name"],
                            "username": data["pinner"]["username"],
                            "followers": data["pinner"]["follower_count"]
                        },
                        "created": data["created_at"],
                        "title": data["title"],
                        "content_domain": data["domain"],
                        "images": data["images"]
                    } for data in resource["data"]["results"]
                ]
            }
        }


    def __search(self, name: str, size: int) -> dict:
        
        response: Response = self.__retry.get(
                url=f'{self.__api}?source_url=/search/pins/?q={name}&rs=typed&data={dumps(self.__create_param(query=name, size=size))}', \
                headers=self.__headers
            )
        
        resource: dict = response.json()["resource_response"]
        if not len(resource["data"]["results"]): return False
        return self.__extract_data(resource=resource, query=name)


    def main(self, name: str, size: int):

        results = self.__search(name=name, size=size)
        if not results: return True

        for ind, url in enumerate(results["content"]["data"]):
            yield url["images"]["orig"]["url"]
