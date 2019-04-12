import flask
import flask_buzz


app = flask.app.Flask(__name__)


def log_error(err):
    flask.current_app.logger.error(str(err))


app.register_error_handler(
    flask_buzz.FlaskBuzz,
    flask_buzz.FlaskBuzz.build_error_handler(log_error),
)


@app.route('/')
def index():
    raise flask_buzz.FlaskBuzz("There's a problem that should be logged")


if __name__ == '__main__':
    app.run()
