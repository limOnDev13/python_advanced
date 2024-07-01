dict_config = {
    'version': 1,
    'disable_existing_loggers': False,
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
        }
    },
    'loggers': {
        'app': {
            'level': 'DEBUG',
            'handlers': ['dif_files'],
            'propagate': False
        },
        'utils': {
            'level': 'DEBUG',
            'handlers': ['dif_files', 'utils_handler'],
            'propagate': False
        }
    }
}
