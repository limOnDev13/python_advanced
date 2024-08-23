from flask import Flask, send_file
from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput
import os


app = Flask(__name__)


@app.route('/get-graph-image')
def get_graph_image():
    graph_path: str = './pycallgraph.png'
    if os.path.exists(graph_path):
        return send_file(graph_path, mimetype='image/png'), 200
    return 'Image not found', 404


@app.route('/hello')
def hello():
    return 'Hello, world!', 200


if __name__ == '__main__':
    with PyCallGraph(output=GraphvizOutput()):
        app.run(debug=True)
