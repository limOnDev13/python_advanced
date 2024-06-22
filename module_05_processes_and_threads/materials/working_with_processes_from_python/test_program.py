import time
import sys


# def main():
#     print('Start program and going to sleep')
#     time.sleep(5)
#     print('Done sleeping 5 seconds. Bye!')


def main():
    print('Print to stdout', file=sys.stderr)
    print('Print to stderr', file=sys.stderr)
    user_input = input()
    print('User input: "{}"'.format(user_input), file=sys.stderr)


if __name__ == '__main__':
    main()
