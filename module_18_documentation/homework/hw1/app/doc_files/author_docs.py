import json
from typing import Callable
from flasgger import swag_from


authors_list_get: dict = {
    "tags": ["authors"],
    "description": "This is an endpoint for obtaining the book list",
    "responses": {
        200: {
            "description": "list of data about books",
            "schema": {
                "type": "array",
                "items": {
                    "$ref": "#/definitions/Author"
                }
            }
        }
    }
}


authors_list_post: dict = {
    "tags": ["authors"],
    "description": "This is an endpoint for author creation.",
    "parameters": [{
        "in": "body",
        "name": "new author params",
        "schema": {"$ref": "#/definitions/Author"}
    }],
    "responses": {
        201: {
            "description": "The author has been created",
            "schema": {
                "$ref": "#/definitions/Author"
            },
        },
        400: {
            "description": "Validation error"
        }
    }
}

one_author_get: dict = {
    "tags": ["authors"],
    "description": "This is an endpoint for obtaining the one author",
    "responses": {
        200: {
            "description": "author data",
            "schema": {
                "$ref": "#/definitions/Author"
            }
        },
        404: {
            "description": "Author not found"
        }
    }
}

one_author_delete: dict = {
    "tags": ["authors"],
    "description": "This is an endpoint for deleting author from database",
    "responses": {
        202: {
            "description": 'Author was deleted from database',
            "schema": {"$ref": "#/definitions/Author"}
        },
        404: {
            "description": "Author not found"
        }
    }
}


DICTS_CACHE: dict = dict()


def _from_json_to_dict(json_file: str) -> None:
    """Функция сохраняет словари документаций из json в кеш"""
    with open(json_file) as file:
        doc_dict: dict = json.loads(file.read())
        title: str = doc_dict['info']['title']
        version: str = doc_dict['info']['version']
        openapi_version: str = doc_dict['swagger']
        for path, info in doc_dict['paths'].items():
            for method, doc in info.items():
                doc['title'] = title
                doc['version'] = version
                doc['openapi_version'] = openapi_version
                DICTS_CACHE['/'.join((path, method))] = doc


def swag_json(json_file: str, api_path: str) -> Callable:
    """
    Функция - декоратор над swag_from. Собирает из json словарь c документацией
    :param json_file: Имя json файла. Файл имеет формат, который генерирует Swagger
    :param api_path: api путь. Например, /api/authors/{id}, где author/{id} - url эндпоинта
    :return:
    """
    if len(DICTS_CACHE) == 0:
        _from_json_to_dict(json_file)

    def wrapper(func: Callable) -> Callable:
        doc_dict = DICTS_CACHE['/'.join((api_path, func.__name__))]

        return swag_from(doc_dict)(func)
    return wrapper
