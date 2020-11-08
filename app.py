from flaskr import create_app
from flaskr.services.scrapper import TinderScrapperService

TinderScrapperService().start_daemon()
application = create_app()
