import logging
import sys
from logging import LogRecord
from string import printable
import logging.handlers


base_formatter = logging.Formatter(fmt='%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s')


class ASCIIFilter(logging.Filter):
    @classmethod
    def is_ascii(cls, text: str) -> bool:
        """Метод определяет, состоит ли text из ASCII или нет"""
        set_text: set[str] = set(text)
        return set_text & set(printable) == set_text

    def filter(self, record: LogRecord) -> bool:
        message: str = base_formatter.format(record)

        return message.isascii() and self.is_ascii(message)


class LevelFileHandler(logging.Handler):
    def emit(self, record: LogRecord) -> None:
        """Сообщение в зависимости от уровня будут отправляться в соответствующие файлы"""
        with open(f'{record.name}_{record.levelname}.log', 'a', encoding='utf-8') as log_file:
            message = self.format(record)

            log_file.write(message + '\n')


def get_logger(name):
    logger = logging.getLogger(name)
    logger.addFilter(ASCIIFilter(name))
    # formatter = logging.Formatter(fmt='%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s')
    # handler = LevelFileHandler()
    # handler.setLevel('DEBUG')
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)
    # logger.setLevel('DEBUG')

    return logger


if __name__ == '__main__':
    tests: list[str] = ['a', '1', ',', '|', '<', '>', 'ÎŒØ∏‡°⁄·°€йцукен']

    for test in tests:
        print(f'{test} - ASCIIFilter.is_ascii = {ASCIIFilter.is_ascii(test)}; .isascii = {test.isascii()}')
