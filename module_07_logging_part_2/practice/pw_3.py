"""Конфиг для логирования pw_2"""
dict_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'base': {
            'format': "<%(name)s> || <%(levelname)s> || <%(message)s>"
                      " || <%(module)s>.<%(funcName)s>:<%(lineno)d> ||| <%(very)s>",
        }
    },
    'handlers': {
        'sub_1_handler': {
            '()': 'pw_4.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'base'
        },
        'root_handler': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'base'
        }
    },
    'loggers': {
        'sub_1': {
            'level': 'DEBUG',
            'handlers': ['sub_1_handler'],
            'propagate': True
        },
        'sub_2': {
            'level': 'WARNING',
            'handlers': [],
            'propagate': False
        },
        'sub_sub_1': {
            'level': 'WARNING',
            'handlers': ['sub_1_handler'],
            'propagate': True
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['root_handler']
    }
}
