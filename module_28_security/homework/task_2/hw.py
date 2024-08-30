HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
  {user_input}
</body>
</html>
"""

from flask import Flask, request, Response


app = Flask(__name__)


@app.route('/', methods=['GET'])
def csp_defense():
    user_input = request.args.get('user_input')
    return HTML.format(user_input=user_input)


@app.after_request
def add_csp(response: Response):
    response.headers['Content-Security-Policy'] = "default-src 'none'"
    return response


if __name__ == '__main__':
    app.run(debug=True)
