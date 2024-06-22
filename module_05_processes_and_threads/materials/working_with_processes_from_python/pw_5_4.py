import subprocess
from subprocess import CompletedProcess
import shlex


def curl_command() -> str:
    command_line: str = 'curl -i -H "Accept: application/json" -X GET https://api.ipify.org?format=json'
    command: list[str] = shlex.split(command_line)
    res: CompletedProcess = subprocess.run(command, capture_output=True)

    ip: str = res.stdout.decode().split('\n')[-1].split(':')
    ip = ip[1][1:-2]
    print(f'IP is {ip}')
    return ip


def ps_command() -> int:
    res: CompletedProcess = subprocess.run(['ps', '-A'], capture_output=True)
    processes: list[str] = res.stdout.decode().split('\n')
    processes = processes[1:-1]
    print(f'Number of processes is {len(processes)}')
    return len(processes)


if __name__ == '__main__':
    curl_command()
    ps_command()
