from flask import Flask, request
from urllib import parse
from logger_helper import base_formatter
import re


app = Flask(__name__)


RECEIVED_LOGS: list[str] = list()


def format_record_dict(record_dict: dict[str, list[str]]) -> str:
    """
    Функция преобразует словарь record в строку. Так как base_formatter.format(logging.makeLogRecord(record_dict))
    не хочет работать, пришлось написать эту функцию
    :param record_dict: Словарь record
    :type record_dict: dict
    :return: Отформатированную строку
    """
    format_log: str = base_formatter.__getattribute__('_fmt')

    while re.search(r'%\((.*?)\)[sd]', format_log):
        format_log: str = re.sub(r'%\((.*?)\)[sd]', lambda x: record_dict[x.group(1)][0], format_log)

    return format_log


@app.route('/log', methods=['POST'])
def log():
    """
    Записываем полученные логи которые пришли к нам на сервер
    return: текстовое сообщение об успешной записи, статус код успешной работы

    """
    # Получим данные
    form_data = request.get_data(as_text=True)
    # Десериализуем данные
    data_object: dict[str, list[str]] = parse.parse_qs(form_data)
    # Важно! parse_qs собирает значения в списки
    # Сохраним данные, преобразованные в строку лога
    RECEIVED_LOGS.append(format_record_dict(data_object))

    return 'Log was received', 200


@app.route('/logs', methods=['GET'])
def logs():
    """
    Рендерим список полученных логов
    return: список логов обернутый в тег HTML <pre></pre>
    """
    return '<br>'.join(RECEIVED_LOGS), 200


if __name__ == '__main__':
    app.run(debug=True)
