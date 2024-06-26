"""
Каждый лог содержит в себе метку времени, а значит, правильно организовав логирование,
можно отследить, сколько времени выполняется функция.

Программа, которую вы видите, по умолчанию пишет логи в stdout. Внутри неё есть функция measure_me,
в начале и в конце которой пишется "Enter measure_me" и "Leave measure_me".
Сконфигурируйте логгер, запустите программу, соберите логи и посчитайте среднее время выполнения функции measure_me.
"""
import logging
import random
from typing import List
import json
import subprocess
from datetime import datetime, timedelta


class JSONAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return json.dumps(msg), kwargs


logger = JSONAdapter(logging.getLogger(__name__))


def get_data_line(sz: int) -> List[int]:
    try:
        logger.debug("Enter get_data_line")
        return [random.randint(-(2 ** 31), 2 ** 31 - 1) for _ in range(sz)]
    finally:
        logger.debug("Leave get_data_line")


def measure_me(nums: List[int]) -> List[List[int]]:
    logger.debug("Enter measure_me")
    results = []
    nums.sort()

    for i in range(len(nums) - 2):
        logger.debug(f"Iteration {i}")
        left = i + 1
        right = len(nums) - 1
        target = 0 - nums[i]
        if i == 0 or nums[i] != nums[i - 1]:
            while left < right:
                s = nums[left] + nums[right]
                if s == target:
                    logger.debug(f"Found {target}")
                    results.append([nums[i], nums[left], nums[right]])
                    logger.debug(
                        f"Appended {[nums[i], nums[left], nums[right]]} to result"
                    )
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif s < target:
                    logger.debug(f"Increment left (left, right) = {left, right}")
                    left += 1
                else:
                    logger.debug(f"Decrement right (left, right) = {left, right}")

                    right -= 1

    logger.debug("Leave measure_me")

    return results


def calculate_average_working_time(log_file: str = 'measure_me_logs.log',
                                   level_start: str = 'DEBUG', message_start: str = 'Enter measure_me',
                                   level_end: str = 'DEBUG', message_end: str = 'Leave measure_me') -> float:
    """
    Функция измеряет среднее время работы программы по лог файлам.
    Функция будет вычитать из времени конечного сообщения время начального
    :param log_file: Имя лог файла
    :type log_file: str
    :param level_start: Уровень логирования, на котором находится стартовое сообщение
    :type level_start: str
    :param message_start: Стартовое сообщение
    :type message_start: str
    :param level_end: Уровень логирования, на котором находится конечное сообщение
    :type level_end: str
    :param message_end: Конечное сообщение
    :type message_end: str
    :return: Время работы программы в микросекундах
    :rtype: float
    """
    # Создадим процессы для поиска начала и конца работы программы
    command_find_start: list[str] = ['grep', '-F',
                                     f'"level": "{level_start}", "message": "{message_start}"', log_file]
    command_find_end: list[str] = ['grep', '-F',
                                   f'"level": "{level_end}", "message": "{message_end}"', log_file]
    proc_find_start = subprocess.Popen(command_find_start, stdout=subprocess.PIPE)
    proc_find_end = subprocess.Popen(command_find_end, stdout=subprocess.PIPE)

    # Получим необходимые логи (их несколько, тк программа запускается несколько раз
    start_log_str: str = proc_find_start.stdout.read().decode()
    end_log_str: str = proc_find_end.stdout.read().decode()

    working_times: list[float] = list()
    # Десириализуем логи и получим из них время начала и конца работы
    for log_start_str, log_end_str in zip(start_log_str.split('\n'), end_log_str.split('\n')):
        if log_start_str == '' or log_end_str == '':
            # Конец файла - пустые строки
            break

        start_time_str: str = json.loads(log_start_str)['time'][:-2]
        end_time_str: str = json.loads(log_end_str)['time'][:-2]
        print(start_time_str)
        print(end_time_str)
        print()

        # Переведем строки в datetime и вычтем - получим время работы
        start_time: datetime = datetime.strptime(start_time_str, "%H:%M:%S.%f")
        end_time: datetime = datetime.strptime(end_time_str, "%H:%M:%S.%f")
        working_time: timedelta = end_time - start_time
        working_times.append(working_time.microseconds)

    if not working_times:
        return 0
    return round(sum(working_times) / len(working_times), 5)


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG", filename=f'measure_me_logs.log', encoding='utf-8',
                        format='{"time": "%(asctime)s.%(msecs)s", "level": "%(levelname)s", "message": %(message)s}',
                        datefmt='%H:%M:%S')
    for it in range(15):

        data_line = get_data_line(10 ** 3)
        measure_me(data_line)
    print(f'Среднее время работы программы: {calculate_average_working_time()}')
