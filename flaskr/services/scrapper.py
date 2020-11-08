import os

import pymongo as pymongo
import requests
from datetime import timedelta
from timeloop import Timeloop

mongo_conn = 'mongodb+srv://{username}:{mongopass}@tinder-insights.1thdi.mongodb.net/{dbname}?retryWrites=true&w' \
             '=majority'.format(username='tinderapp', mongopass=os.environ['MONGO_PASS'], dbname='tinderinsights')
client = pymongo.MongoClient(mongo_conn)

api = os.getenv('API_TINDER')

tl = Timeloop()


class TinderScrapperService:

    def __init__(self):
        print('Starting daemon')
        pass

    @staticmethod
    @tl.job(interval=timedelta(seconds=5))
    def scrap_profile():
        response = requests.get("https://api.gotinder.com/profile",
                                headers={'x-auth-token': api})
        db = client.tinderinsights
        try:
            result = db.profile.insert(response.json())
        except pymongo.errors.DuplicateKeyError:
            print('No variations')

    def start_daemon(self):
        tl.start(block=True)


if __name__ == "__main__":
    tss = TinderScrapperService()
    tss.start_daemon()
