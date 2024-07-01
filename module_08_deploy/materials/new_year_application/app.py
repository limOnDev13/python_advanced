import os

from flask import Flask, render_template, send_from_directory

root_dir = os.path.dirname(os.path.abspath(__file__))

template_folder = os.path.join(root_dir, "templates")

app = Flask(__name__, template_folder=template_folder)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/static/<type_dir>/<path:path>')
def send_static(type_dir: str, path: str):
    static_directory = os.path.join(template_folder, 'static')
    required_directory = os.path.join(static_directory, type_dir)

    return send_from_directory(required_directory, path)


if __name__ == "__main__":
    app.run()
