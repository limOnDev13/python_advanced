"""Конфиг для логгера"""
dict_config: dict = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'base': {
            'format': '%(levelname)s | %(message)s'
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
        'module_logger': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False
        }
    }
}
