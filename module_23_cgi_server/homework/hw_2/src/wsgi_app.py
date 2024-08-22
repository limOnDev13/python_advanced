from typing import Callable, Any, Iterable, Optional, Type, Union, List, Dict, Tuple
import re
import json


class WSGIApp:
    def __init__(self) -> None:
        self.routes: Dict[str, Callable] = {}

    @classmethod
    def check_correct_url(cls, url: str) -> str:
        """Функция проверяет корректность url в роуте."""
        url_words: List[str] = url.split('/')
        for word in url_words:
            if ('<' not in word and '>' not in word) or word == '':
                continue
            elif not re.fullmatch(r'(<string:\w+>)|(<\w+>)|(<int:\w+)|(<float:\w+>)', word):
                raise ValueError(f'url must have format /my/url/<[string | int | float]:[var_name]>. Your url: {url}')

        return url

    def route(self, url) -> Callable:
        """Метод - обертка. Добавляет оборачиваемую функцию в self.routes с ее url"""
        def wrapper(func: Callable) -> Any:
            self.routes[self.check_correct_url(url)] = func
            return func
        return wrapper

    @classmethod
    def _kwarg_from_url(cls, input_param: str, param_data: str) -> Optional[Dict[str, Union[str, int, float]]]:
        """
        Функция определяет, подходит ли введенная переменная под описания из url
        Т.е. если input_param = '1', param_data = <string:name>, то вернет True, если param_data = <float:name>,
        то вернет False. Также param_data может придти в формате <name> (без указания типа) -
        будет подразумеваться тип str. Возможные типы: string, int, float
        :param input_param: Параметр, переданный через url
        :param param_data: Описание параметра url. Имеет формат <type:name>, возможные значения type - string, float, int
        :return: Если переданное значение параметра подходит под описание param_data,
        то вернет словарь {name: type(input_param)}, чтобы передать переменную в функцию как kwargs
        """
        # param_data имеет формат <type:name> - уберем скобки и разделим по ':'
        param_info: List[str] = param_data[1:-1].split(':')

        # Если передано только имя переменной, то ее тип будет str
        if len(param_info) == 1:
            param_type: Type = str
        # Первый элемент param_info - описание типа переменной
        else:
            param_type_str: str = param_info[0]
            if param_type_str == 'float':
                param_type: Type = str
            elif param_type_str == 'int':
                param_type: Type = int
            else:
                param_type: Type = str

        # Последний элемент param_info - имя переменной
        param_name: str = param_info[-1]
        # Вернем kwarg. Сразу преобразуем к указанному типу, если что не так, то python выбросит исключение TypeError
        return {param_name: param_type(input_param)}

    def _search_func(self, url: str) -> Optional[Tuple[Callable, Dict[str, Any]]]:
        """
        Метод сопоставляет url с имеющимися в self.routes.keys() с учетом переданных переменных через url.
        Если метод не найдет url - вернет None, иначе вернет сохраненную функцию под этим url и ее kwargs
        :param url: url (включая параметры, т.е. подобные /some/url/<string:with>/<int:vars>)
        :return: Если url есть в self.routes, то вернет сохраненную функцию и kwargs из url (если таковые имеются)
        """
        # Посмотрим, нет ли url в списке self.routes.keys()
        if url in self.routes.keys():
            return self.routes[url], {}  # Если нашли url, то в нее не передавали никаких переменных

        cur_url: str = url
        while cur_url != '':
            if cur_url[-1] == '/':
                cur_url = cur_url[:-1]
            else:
                match = re.match(r'.*/(.*)$', cur_url)
                if match:
                    cur_url = cur_url[: -len(match.group(1))]
                else:
                    raise ValueError(f'No matches, cur_url = {cur_url}')

            for saved_url in self.routes.keys():
                if saved_url.startswith(cur_url):
                    input_params_str: str = url[len(cur_url):]
                    params_data_str: str = saved_url[len(cur_url):]

                    input_params: List[str] = input_params_str.split('/')
                    params_data: List[str] = params_data_str.split('/')
                    if len(input_params) != len(params_data):
                        continue

                    kwargs: Dict[str, Any] = dict()
                    for input_param, param_data in zip(input_params, params_data):
                        if input_param == '' and param_data == '':
                            continue
                        try:
                            kwargs.update(self._kwarg_from_url(input_param, param_data))
                        except Exception:
                            break
                    else:
                        return self.routes[saved_url], kwargs
        else:
            return None

    def __call__(self, environ: Dict, start_response: Callable) -> Iterable:
        request_url: str = environ.get('REQUEST_URI', '/')
        print('-' * 30)
        print(request_url)
        print('-' * 30)
        func_and_kwargs: Optional[Tuple[Callable, Dict]] = self._search_func(request_url)
        if func_and_kwargs:
            func, kwargs = func_and_kwargs
            status: str = '200 OK'
            response = func(**kwargs)
        else:
            status: str = '404'
            response = json.dumps({'description': 'PAGE NOT FOUND'})

        start_response(status, [('Content-type', 'Application/json')])
        return response.encode('utf-8')
