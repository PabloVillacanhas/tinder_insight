from datetime import datetime
from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import os
import logging.config
import jinja2

from flaskr.services.credentials import load
from flaskr.services import scrapper

logger = None


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    global logger

    if app.config['ENV'] == 'production':
        app.config.from_pyfile('config.py')
    elif app.config['ENV'] == 'development':
        app.config.from_pyfile('devconfig.py')

    logging.config.dictConfig(app.config['LOGGING_CONFIG'])
    logger = logging.getLogger(app.config['FLASK_APP'])

    secrets = None
    try:
        secrets = load()
        logger.info('Secrets loaded successfully')
    except Exception as e:
        logger.exception(e)

    mongo_connection = 'mongodb+srv://{username}:{mongopass}@tinder-insights.1thdi.mongodb.net/{dbname}?retryWrites=true&w' \
                       '=majority'.format(username='tinderapp', mongopass=secrets['MONGO_PASS_TINDER'],
                                          dbname='tinderinsights')

    scrapper_service = scrapper.ScrapperService(mongo_connection, secrets['API_TINDER'])
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(scrapper_service.scrap_profile, 'interval', seconds=5)
    scheduler.start()

    logger.info('Application started')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #Jinja filters
    def uptime(from_date):
        td = datetime.utcnow() - from_date
        return '{0} days, {1} hours, {2} minutes and {3} seconds.'.format(td.days, td.seconds // 3600,
                                                                          td.seconds % 3600 // 60, td.seconds % 60)
    app.jinja_env.filters['uptime'] = uptime

    @app.route('/')
    def hello_world():
        return render_template('index.html.jinja2', scrapper=scrapper_service)

    return app
