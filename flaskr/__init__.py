from pprint import pprint

from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import os

from flaskr.services import scrapper


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    mongo_connection ='mongodb+srv://{username}:{mongopass}@tinder-insights.1thdi.mongodb.net/{dbname}?retryWrites=true&w' \
                          '=majority'.format(username='tinderapp', mongopass=os.environ['MONGO_PASS_TINDER'],
                                             dbname='tinderinsights')

    scrapper_service = scrapper.ScrapperService(mongo_connection)
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(scrapper_service.scrap_profile, 'interval', seconds=5)
    scheduler.start()

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello_world():
        return 'Hola a todo el mundo'

    @app.route('/api')
    def apikey():
        return os.getenv('API_TINDER', 'none')

    return app
