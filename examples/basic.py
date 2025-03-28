"""
This example shows a basic Flask app with a registered error handler for FlaskBuzz.

When you attempt to access the root route, a FlaskBuzz exception will be raised.
Due to the provided error handler, a nicely formatted error response will be returned.
"""

import flask
from flask_buzz import FlaskBuzz


app = flask.app.Flask(__name__)
app.register_error_handler(*FlaskBuzz.build_error_handler())


@app.route('/')
def index():
    raise FlaskBuzz("Something went wrong")


if __name__ == '__main__':
    app.run()
