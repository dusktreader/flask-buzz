import pytest
import flask
import flask_buzz


class OverloadBuzz(flask_buzz.FlaskBuzz):
    status_code = 401


@pytest.fixture(scope='session')
def app():
    app = flask.Flask('normal_app')
    app.debug = False
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'test_server'

    @app.route('/')
    def index():
        raise flask_buzz.FlaskBuzz('basic test')

    @app.route('/status')
    def status():
        raise OverloadBuzz('status test')

    app.register_error_handler(
        flask_buzz.FlaskBuzz,
        flask_buzz.FlaskBuzz.build_error_handler(
            lambda e: print('message: ', e.message),
            lambda e: print('status_code: ', e.status_code),
        ),
    )

    with app.app_context():
        yield app
