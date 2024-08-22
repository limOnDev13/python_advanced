from wsgi_app import WSGIApp
import os
import json


application = WSGIApp()


@application.route('/env')
def environ_():
    # return json.dumps(dict(os.environ))
    return json.dumps(dict(os.environ))


@application.route('/hello/<username>')
@application.route('/hello')
def hello_world(username: str = 'World'):
    return json.dumps({'Body': f'Hello, {username}!'})
