import pytest
import flask
import flask_buzz


class OverloadBuzz(flask_buzz.FlaskBuzz):
    status_code = 401


@pytest.fixture(scope='session')
def app():
    app = flask.Flask(__name__)
    app.debug = False
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'test_server'

    @app.route('/')
    def index():
        raise flask_buzz.FlaskBuzz('basic test')

    @app.route('/status')
    def status():
        raise OverloadBuzz('status test')

    app.register_error_handler(flask_buzz.FlaskBuzz, flask_buzz.error_handler)

    with app.app_context():
        yield app
