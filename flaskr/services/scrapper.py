import os
import json
from pprint import pprint

import pymongo as pymongo
import requests

from flaskr.models import tinder_profile_from_dict


class ScrapperService:
    api = os.getenv('API_TINDER')

    def __init__(self, mongo_conn):
        self.client = pymongo.MongoClient(mongo_conn)
        self._last_document = None

    @property
    def last_profile(self):
        if self._last_document is None:
            db = self.client.tinderinsights
            self._last_document = db.tinderinsights.find().sort({"_id": 1})
            return tinder_profile_from_dict(json.loads(self._last_document))
        else:
            return tinder_profile_from_dict(json.loads(self._last_document))

    def should_upload(self, response):
        new_profile = tinder_profile_from_dict(json.loads(response))
        last_profile = tinder_profile_from_dict(json.loads(self._last_document))
        return not new_profile.__eq__(last_profile)

    def scrap_profile(self):
        print("Scheduler is alive!")
        response = requests.get("https://api.gotinder.com/profile",
                                headers={'x-auth-token': ScrapperService.api})
        if response.status_code == 200:
            if self.should_upload(response):
                self.upload_to_mongo(response)

    def upload_to_mongo(self, response):
        db = self.client.tinderinsights
        try:
            result = db.profile.insert(json.loads(response.content))
            print(result)
        except pymongo.errors.DuplicateKeyError as e:
            pprint(e)
            print('No variations')
