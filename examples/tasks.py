"""
This example shows a basic Flask app with a registered error handler that executes tasks upon activation.

Any time a `FlaskBuzz` exception (or any descendant classes) is handled, the registered tasks are also executed.
Each task can be any callable that accepts a single argument, which will be the handled error.

In this example, every call to the root path will result in the raised error being logged and printed.
"""

import flask
from flask_buzz import FlaskBuzz


app = flask.app.Flask(__name__)


def log_error(err: FlaskBuzz):
    flask.current_app.logger.error(err)


def print_error(err: FlaskBuzz):
    print(err)


app.register_error_handler(*FlaskBuzz.build_error_handler(log_error, print_error))


@app.route('/')
def index():
    raise FlaskBuzz("There's a problem that should be logged and printed")


if __name__ == '__main__':
    app.run()
