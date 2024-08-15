"""Модуль отвечает за конфиг логирования"""
dict_config: dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'base': {
            'format': '%(thread)d | %(module)s | %(funcName)s | %(asctime)s | %(levelname)s: %(message)s'
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
        'app_logger': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False
        },
        'tasks_logger': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False
        },
        'utils_logger': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False
        },

    }
}
