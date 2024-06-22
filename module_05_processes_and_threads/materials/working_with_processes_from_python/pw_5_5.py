import subprocess
from subprocess import Popen
import shlex
import time


def ps_command_with_popen() -> int:
    proc: Popen = Popen(['ps', '-A'], stdout=subprocess.PIPE)
    proc.wait()
    processes: list[str] = proc.stdout.read().decode().split('\n')
    processes = processes[1:-1]
    print(f'Number of processes is {len(processes)}')
    return len(processes)


def some_sleep() -> None:
    start_time: float = time.time()
    command_line: str = 'sleep 1 && echo "My mission is done here!"'

    processes: list[Popen] = list()
    for _ in range(15):
        processes.append(Popen(command_line, shell=True))

    for num, proc in enumerate(processes):
        proc.wait()

    print('Время работы программы:', time.time() - start_time)


def sleep_and_exit() -> Popen:
    command_line: str = 'sleep 3 && exit 1'

    proc: Popen = Popen(command_line, shell=True)
    return proc


if __name__ == '__main__':
    ps_command_with_popen()
    some_sleep()
    print(sleep_and_exit().wait())
    print(sleep_and_exit().wait(timeout=2))
