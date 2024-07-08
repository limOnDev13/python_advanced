import subprocess
import shlex
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def process_count(username: str) -> int:
    # количество процессов, запущенных из-под
    # текущего пользователя username
    command_line: str = f'pgrep -u {username} | wc -l'
    res = subprocess.run(command_line, capture_output=True, shell=True)
    return int(res.stdout.decode().split('\n')[0])


def total_memory_usage(root_pid: int, depth: int = 0) -> float:
    """Функция рекурсивно получает rss древа процессов"""
    # суммарное потребление памяти древа процессов
    # с корнем root_pid в процентах
    used_memory: int = 0

    # 1) получим размер памяти самого процесса
    get_parent_process_memory_command: str = f'ps --pid {root_pid} -o rss'
    res = subprocess.run(shlex.split(get_parent_process_memory_command), capture_output=True)
    command_result: str = res.stdout.decode()
    try:
        used_memory += int(command_result.split('\n')[1])
    except ValueError:
        return 0

    # 2) получим список всех дочерних процессов
    get_list_child_processes_command: str = f'ps --ppid {root_pid} -o pid'
    res = subprocess.run(shlex.split(get_list_child_processes_command), capture_output=True)
    command_result: str = res.stdout.decode()

    # Пропускаем заголовок и последнюю пустую строку
    list_cpid: list[int] = [int(line.rstrip().lstrip()) for line in command_result.split('\n')[1:-1]]
    logger.debug(f'Current PID is {root_pid}. Child PIDs is {list_cpid}')
    if not list_cpid:
        return 0
    for pid in list_cpid:
        used_memory += total_memory_usage(pid, depth + 1)

    # 3) Получим объем доступной памяти
    if depth == 0:
        res = subprocess.run('free', capture_output=True)
        memory = int(res.stdout.decode().split('\n')[1].split()[1])
        return used_memory / memory * 100

    return used_memory


if __name__ == "__main__":
    pid: int = 1
    username: str = 'root'
    print(f'Количество процессов, запущенных из-под текущего пользователя {username} равно {process_count(username)}')
    print(f'Процесс с pid {pid} и все его дочерние процессы занимают {round(total_memory_usage(pid), 2)}% памяти')
