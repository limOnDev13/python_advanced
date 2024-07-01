dict_config = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'base': {
            'format': '%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s'
        }
    },
    'handlers': {
        'dif_files': {
            '()': 'logger_helper.LevelFileHandler',
            'level': 'DEBUG',
            'formatter': 'base'
        },
        'utils_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'filename': 'utils.log',
            'when': 'h',
            'interval': 10,
            'backupCount': 3,
            'formatter': 'base',
        },
        'flask_handler': {
            'class': 'logging.handlers.HTTPHandler',
            'host': 'localhost:5000',
            'url': '/log',
            'method': 'POST'
        }
    },
    'loggers': {
        'app': {
            'level': 'DEBUG',
            'handlers': ['dif_files', 'flask_handler'],
            'propagate': True
        },
        'utils': {
            'level': 'DEBUG',
            'handlers': ['dif_files', 'utils_handler', 'flask_handler'],
            'propagate': True
        }
    }
}
