"""
This example shows a basic Flask app with a registered error handler for A custom FlaskBuzz derived class.

With the error handler registered only for the CustomError class, only exceptions of that class and its descendents will
be handled. Note that in the `ChildError` class, it's message is hard-coded. This pattern can be used if you want an
exception to have a default message.
"""

from typing import Any
import flask
from flask_buzz import FlaskBuzz


class CustomError(FlaskBuzz):
    status_code: int = 400


class ChildError(CustomError):
    status_code: int = 422

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__('child error handled!', *args, **kwargs)


app = flask.app.Flask(__name__)
app.register_error_handler(*CustomError.build_error_handler())


@app.route('/custom')
def custom():
    raise CustomError("custom error handled!")


@app.route('/child')
def child():
    raise ChildError()


@app.route('/other')
def other():
    raise RuntimeError("regular error not handled")


if __name__ == '__main__':
    app.run()
