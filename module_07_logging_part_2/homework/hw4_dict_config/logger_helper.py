import logging
import sys
from logging import LogRecord


class LevelFileHandler(logging.Handler):
    def emit(self, record: LogRecord) -> None:
        """Сообщение в зависимости от уровня будут отправляться в соответствующие файлы"""
        with open(f'{record.name}_{record.levelname}.log', 'a', encoding='utf-8') as log_file:
            message = self.format(record)

            log_file.write(message + '\n')


def get_logger(name):
    logger = logging.getLogger(name)
    # formatter = logging.Formatter(fmt='%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s')
    # handler = LevelFileHandler()
    # handler.setLevel('DEBUG')
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)
    # logger.setLevel('DEBUG')

    return logger
