import json
import requests
import logging
import pymongo as pymongo
from datetime import datetime
from bson.objectid import ObjectId

from flaskr.models import tinder_profile_from_dict, TinderProfile

logger = logging.getLogger(__name__)


class ScrapperService:

    def __init__(self, mongo_conn, tinder_api):
        self.client = pymongo.MongoClient(mongo_conn)
        self._last_document = None
        self.api = tinder_api
        self.status = 'WORKING'
        self.start = datetime.utcnow()
        self.last_execution = datetime.utcnow()

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
        logger.info('Scrapping')
        response = requests.get("https://api.gotinder.com/profile",
                                headers={'x-auth-token': self.api})
        if response.status_code == 200:
            self.last_execution = datetime.utcnow()
            if self.should_upload(response.content):
                self.upload_to_mongo(response.content)
            else:
                logger.info('No variations')
        elif response.status == 401:
            logger.warning('The token has expired')
            self.status = 'IDLE'

    def upload_to_mongo(self, response):
        db = self.client.tinderinsights
        try:
            logger.info('Uploading to mongo')
            self._last_document = json.loads(response)
            self._last_document["_id"] = str(ObjectId())
            db.profile.insert(self._last_document)
        except Exception as e:
            logging.error(e)
