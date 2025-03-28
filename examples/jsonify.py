"""
This example shows a basic Flask app where the `jsonify()` method of a `FlaskBuzz` derived class is called explicitly.

Note that in addition to the normal fields that are packaged by an error handler, an additional field named "origin" is
included. The `jsonify()` method can accept arbitrary keyword arguments as long as they are JSON serializable.
"""

from typing import Any
import flask
import http
from flask_buzz import FlaskBuzz

app = flask.app.Flask(__name__)


class InvalidParameters(FlaskBuzz):
    status_code: int = http.HTTPStatus.PRECONDITION_FAILED


def check_params(id: int | None = None, **_):
    if not id:
        raise InvalidParameters('id field must be defined')


@app.route('/')
def index():
    params: dict[str, Any] = flask.request.args
    try:
        check_params(**params)
        return flask.jsonify(message='All good!')
    except InvalidParameters as err:
        return err.jsonify(origin="index")


if __name__ == '__main__':
    app.run()
