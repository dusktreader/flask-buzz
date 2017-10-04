import flask
import flask_buzz

app = flask.app.Flask(__name__)
app.register_error_handler(flask_buzz.FlaskBuzz, flask_buzz.error_handler)


class MyException(flask_buzz.FlaskBuzz):
    status_code = 403

    def __init__(self, *args, **kwargs):
        super().__init__('hard coded message', *args, **kwargs)


def do_stuff():
    raise MyException()


@app.route('/')
def index():
    do_stuff()


if __name__ == '__main__':
    app.run()
