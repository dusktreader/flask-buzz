import flask
import flask_buzz
import http

app = flask.app.Flask(__name__)
app.register_error_handler(flask_buzz.FlaskBuzz, flask_buzz.error_handler)


class InvalidParameters(flask_buzz.FlaskBuzz):
    status_code = http.HTTPStatus.PRECONDITION_FAILED


def check_params(id=None, **params):
    if not id:
        raise InvalidParameters('id field must be defined')


@app.route('/')
def index():
    params = flask.request.args
    try:
        check_params(**params)
        return flask.jsonify(message='All good!')
    except flask_buzz.FlaskBuzz as err:
        return err.jsonify()


if __name__ == '__main__':
    app.run()
