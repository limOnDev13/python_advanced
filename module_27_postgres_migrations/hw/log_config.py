dict_config: dict = {
    'version': 1,
    'disable_existing_loggers': True,
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
        'init_logger': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False
        }
    }
}