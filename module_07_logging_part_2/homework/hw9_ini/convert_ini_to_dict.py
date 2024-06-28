"""Модуль для перевода ini конфига в dict конфиг.
Я пока не разобрался как перевести ini в dict по-простому, поэтому в лоб прочитал файл и собрал словарь
"""
from typing import Optional
import configparser
import json
import re


def get_items_from_section_with_key(config: configparser.ConfigParser,
                                    section_name: str) -> dict:
    """
    Если у секции есть опция 'keys', то функция собирает для этой секции словари по этим ключам.
    :param config: Конфиг
    :param section_name: название секции
    :return: словарь переданного ключа
    """
    result_dict: dict = dict()

    if not config.has_section(section_name):
        raise IndexError(f'Секции {section_name} нет в конфиге')

    for option in config[section_name]:
        if option == 'args':
            result_dict[option] = re.findall(r"[^()',]+", config[section_name][option])
        if option == 'propagate':
            if config[section_name][option] == '0':
                result_dict[option] = False
            else:
                result_dict[option] = True
        elif ',' in config[section_name][option]:
            result_dict[option] = config[section_name][option].split(',')
        else:
            result_dict[option] = config[section_name][option]

    return result_dict


def compile_dict_params(config: configparser.ConfigParser, param: str) -> dict:
    result_dict: dict = dict()

    if config.has_section(param):
        # Если есть ключи - создадим словари по этим ключам
        if config.has_option(param, 'keys'):
            for key in config[param]['keys'].split(','):
                result_dict[key] = get_items_from_section_with_key(config, f'{param[:-1]}_{key}')

    return result_dict


def convert_ini_config_to_dict(ini_file: str = 'logging_conf.ini',
                               file_with_dict: Optional[str] = 'logging_dict.py') -> dict:
    """
    Функция считывает конфигурацию из файла ini с конфигом и переводит конфиг в словарь.
    Если указан параметр file_with_dict, то поэтому пути функция сохраняет словарь.
    :param ini_file: Путь до файла ini с конфигом логирования
    :type ini_file: str
    :param file_with_dict: Путь до файла, куда сохранить полученный словарь.
    Если None - функция просто вернет словарь
    :type file_with_dict: Optional[str]
    :return: Словарь с конфигом логирования
    :rtype: dict
    """
    result_dict: dict = dict()

    config = configparser.RawConfigParser()
    with open(ini_file, 'r', encoding='utf-8') as config_file:
        config.read_file(config_file)

        # Я пока не разобрался в configparser, поэтому буду собирать словарь по необходимым ключам
        # Версия
        if config.has_section('version'):
            result_dict['version'] = config['version']
        else:
            result_dict['version'] = 1
        # Отключение существующих логгеров
        if config.has_section('disable_existing_loggers'):
            if config['disable_existing_loggers'] == '0':
                result_dict['disable_existing_loggers'] = False
            else:
                result_dict['disable_existing_loggers'] = True
        else:
            result_dict['disable_existing_loggers'] = False
        # Форматтеры
        result_dict['formatters'] = compile_dict_params(config, 'formatters')
        # Хэндлеры
        result_dict['handlers'] = compile_dict_params(config, 'handlers')
        # Логгеры
        result_dict['loggers'] = compile_dict_params(config, 'loggers')

    if file_with_dict:
        with open(file_with_dict, 'w', encoding='utf-8') as output:
            output.write(f'config_dict: dict = {result_dict}')
            output.write('\n')

    return result_dict


if __name__ == '__main__':
    print(json.dumps(convert_ini_config_to_dict(), indent=2))
