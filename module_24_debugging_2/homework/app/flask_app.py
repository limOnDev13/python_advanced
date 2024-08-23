import time
import random

from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)


@app.route('/hello_world')
@metrics.counter('count_successful_responses', 'Count num of calls',
                 labels={'status_code': lambda response: response.status_code})
def hello_world():
    flag = random.choice((True, False))
    if flag:
        return 'Hello, world!', 200
    else:
        return 'Sorry, failure', 400


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, threaded=True)
