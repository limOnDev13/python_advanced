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
            'handlers': ['dif_files'],
            'propagate': False
        }
    }
}
