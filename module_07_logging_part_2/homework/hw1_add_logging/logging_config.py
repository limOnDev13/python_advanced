dict_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'base': {
            'format': '%(name)s | %(levelname)s | %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'base'
        }
    },
    'loggers': {
        'app': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False
        },
        'utils': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False
        }
    }
}
