FLASK_APP = 'tinder_insights'
EXPLAIN_TEMPLATE_LOADING = True
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
        'apscheduler': {
            'level': 'WARNING',
            'propagate': False
        },
    }
}
