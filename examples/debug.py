"""
This example shows a basic Flask app with a registered error handler for FlaskBuzz that is running in debug mode.

When you attempt to access the root route, a FlaskBuzz exception will be raised.
Due to the provided error handler, a nicely formatted error response will be returned.
The response body will include the full message from the handled error (instead of just the `base_message`),
as well as a string representation of the handled error and the response headers.
"""

import flask
from flask_buzz import FlaskBuzz


app = flask.app.Flask(__name__)
app.register_error_handler(*FlaskBuzz.build_error_handler())
FlaskBuzz.debug = True


@app.route('/')
def index():
    with FlaskBuzz.handle_errors("Something went wrong"):
        raise RuntimeError("Boom!")


if __name__ == '__main__':
    app.run()
