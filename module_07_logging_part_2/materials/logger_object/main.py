import logging
import flask

from http_utils import get_ip_address
from subprocess_utils import get_kernel_version
import http_utils
import subprocess_utils


logging.basicConfig(level='DEBUG')
main_logger = logging.getLogger('main')
main_logger.setLevel('INFO')
utils_logger = logging.getLogger('utils')
utils_logger.setLevel('DEBUG')
print(http_utils.logger)
print(http_utils.logger.parent)
print(http_utils.logger.parent.parent)
print(subprocess_utils.logger)
print(subprocess_utils.logger.parent)
print(subprocess_utils.logger.parent.parent)


app = flask.Flask(__name__)


@app.route('/get_system_info')
def get_system_info():
    logger.info('Start working')
    ip = get_ip_address()
    kernel = get_kernel_version()
    return "<p>{}</p><p>{}</p>".format(ip, kernel)


if __name__ == '__main__':
    app.run(debug=True)
