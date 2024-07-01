import logging
from logging import LogRecord
import sys
from typing import IO


class StreamHandler(logging.Handler):
    def __init__(self, stream: IO = sys.stderr):
        super().__init__()
        self.stream: IO = stream

    def emit(self, record: LogRecord) -> None:
        message = self.format(record)
        print(record)
        print(vars(record))
        print('-----------------')
        self.stream.write(message + '\n')
