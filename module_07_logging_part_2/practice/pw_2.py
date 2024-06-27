import logging

# 1
root_logger = logging.getLogger()
sub_1_logger = logging.getLogger('sub_1')
sub_2_logger = logging.getLogger('sub_2')
sub_sub_1_logger = logging.getLogger('sub_1.sub_sub_1')

# 2
sub_1_handler = logging.StreamHandler()
sub_1_handler.setLevel('DEBUG')
sub_1_logger.addHandler(sub_1_handler)
sub_sub_1_logger.addHandler(sub_1_handler)

# 3
formatter = logging.Formatter(fmt="<%(name)s> || <%(levelname)s> || <%(message)s>"
                                  " || <%(module)s>.<%(funcName)s>:<%(lineno)d>")
sub_1_handler.setFormatter(formatter)

# 4
root_handler = logging.StreamHandler()
root_handler.setLevel('DEBUG')
root_handler.setFormatter(formatter)
root_logger.addHandler(root_handler)

# 5
sub_2_logger.propagate = False


def main():
    root_logger.critical('root_logger said what?')
    sub_1_logger.critical('sub_1_logger said what?')
    sub_sub_1_logger.critical('sub_sub_1_logger said what?')
    sub_2_logger.critical('sub_2_logger said what?')


if __name__ == '__main__':
    main()
