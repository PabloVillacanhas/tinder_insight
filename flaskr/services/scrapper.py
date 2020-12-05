import os
import json

import pymongo as pymongo
from bson.objectid import ObjectId
import requests

from flaskr.models import tinder_profile_from_dict, TinderProfile


class ScrapperService:
    api = os.getenv('API_TINDER')

    def __init__(self, mongo_conn):
        self.client = pymongo.MongoClient(mongo_conn)
        self._last_document = None

    @property
    def last_profile(self) -> TinderProfile:
        if self._last_document is None:
            db = self.client.tinderinsights
            self._last_document = db.profile.find_one(sort=[("_id", pymongo.DESCENDING)])
        return tinder_profile_from_dict(self._last_document)

    def should_upload(self, response_content):
        new_profile = tinder_profile_from_dict(json.loads(response_content))
        return not new_profile.__eq__(self.last_profile)

    def scrap_profile(self):
        print("Scheduler is alive!")
        response = requests.get("https://api.gotinder.com/profile",
                                headers={'x-auth-token': ScrapperService.api})
        if response.status_code == 200:
            if self.should_upload(response.content):
                self.upload_to_mongo(response.content)
            else:
                print('No variations')

    def upload_to_mongo(self, response):
        db = self.client.tinderinsights
        try:
            self._last_document = json.loads(response)
            self._last_document["_id"] = str(ObjectId())
            db.profile.insert(self._last_document)
        except Exception as e:
            print(e)
