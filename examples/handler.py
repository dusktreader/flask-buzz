import flask
import flask_buzz


app = flask.app.Flask(__name__)


app.register_error_handler(
    flask_buzz.FlaskBuzz,
    flask_buzz.FlaskBuzz.build_error_handler(),
)


@app.route('/')
def index():
    raise flask_buzz.FlaskBuzz('Nope!')


if __name__ == '__main__':
    app.run()
