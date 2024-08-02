import operator
from flask import Flask
from flask_jsonrpc import JSONRPC
from flask_jsonrpc.exceptions import InvalidParamsError
from flasgger import Swagger, APISpec
from apispec_webframeworks.flask import FlaskPlugin


spec = APISpec(
    title='Calc',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[FlaskPlugin()]
)


app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)


@jsonrpc.method('calc.add')
def add(a: float, b: float) -> float:
    """
    This is a method for adding numbers
    ---
    tags:
      - calc
    responses:
      200:
        description: Sum of tho numbers,
        schema:
          $ref: '#definitions/Jsonrpc'
    """
    return operator.add(a, b)


@jsonrpc.method('calc.subtract')
def sub(a: float, b: float) -> float:
    """
    This is a method for subtracting numbers
    ---
    tags:
      - calc
    responses:
      200:
        description: The difference between two numbers
        schema:
          $ref: '#definitions/Jsonrpc'
    """
    return operator.sub(a, b)


@jsonrpc.method('calc.multiply')
def mul(a: float, b: float) -> float:
    """
    This is a method for multiplication numbers
    ---
    tags:
      - calc
    responses:
      200:
        description: The product of two numbers
        schema:
          $ref: '#definitions/Jsonrpc'
    """
    return operator.mul(a, b)


@jsonrpc.method('calc.divide')
def div(a: float, b: float) -> float:
    """
    This is a method for dividing numbers
    ---
    tags:
      - calc
    responses:
      200:
        description: The quotient of two numbers
        schema:
          $ref: '#definitions/Jsonrpc'
    """
    if b == 0.0:
        raise InvalidParamsError(message='Zero Division', code=666)
    return operator.truediv(a, b)


template = spec.to_flasgger(app)
template['definitions'] = {
    'jsonrpc_request': {
        "type": "object",
        "required": ['jsonrpc', 'method', 'params', 'id'],
        'properties': {
            'jsonrpc': {
                'type': 'string',
                'default': '2.0',
                'pattern': '2.0',
            },
            'method': {
                'type': 'string',
                'enum': ['calc.add', 'calc.subtract', 'calc.multiply', 'calc.divide']
            },
            'params': {
                'type': 'object',
                'required': ['a', 'b'],
                'properties': {
                    'a': {'type': 'number'},
                    'b': {'type': 'number'}
                }
            },
            'id': {'type': 'string'}
        }
    },
    'jsonrpc_response': {
        "type": "object",
        "required": ['jsonrpc', 'id'],
        'properties': {
            'jsonrpc': {
                'type': 'string',
                'default': '2.0',
                'pattern': '2.0',
            },
            'result': {'type': 'number'},
            'id': {'type': 'string'}
        }
    },
}
template['paths'] = {
    '/api': {
        'post': {
            'description': 'This is JSON-RPC endpoint for working with calc',
            'parameters': [
                {
                    'in': 'body',
                    'name': 'params for calc methods',
                    'schema': {'$ref': '#/definitions/jsonrpc_request'}
                }
            ],
            'tags': ['calc'],
            'responses': {
                200: {
                    'description': 'Result of calculations',
                    'schema': {'$ref': '#/definitions/jsonrpc_response'}
                }
            }
        }
    }
}
swagger = Swagger(app, template=template)


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
