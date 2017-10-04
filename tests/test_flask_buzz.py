import flask
import flask_buzz
import json
import pytest


class OverloadBuzz(flask_buzz.FlaskBuzz):
    status_code = 401


@pytest.fixture(scope='session')
def app():
    app = flask.app.Flask('TestFlaskBuzzApp')
    app.testing = True
    app.config.from_mapping(SERVER_NAME='test_server')

    @app.route('/')
    def index():
        raise flask_buzz.FlaskBuzz('basic test')

    @app.route('/status')
    def status():
        raise OverloadBuzz('status test')

    app.register_error_handler(flask_buzz.FlaskBuzz, flask_buzz.error_handler)

    with app.app_context():
        yield app


class TestFlaskBuzz:

    def test_raise(self):
        with pytest.raises(flask_buzz.FlaskBuzz) as err_info:
            raise flask_buzz.FlaskBuzz('i failed')
        assert 'i failed' in str(err_info.value)

    def test_basic_functionality(self, app):
        """
        This test verifies that the basic functionality of FlaskBuzz works
        correctly. Verifies that the exception jsonifies correctly when it
        is bound to an error handler.
        """
        client = app.test_client()
        response = client.get(flask.url_for('index'))
        assert response.status_code == flask_buzz.FlaskBuzz.status_code
        response_json = json.loads(response.get_data(as_text=True))
        assert response_json['message'] == 'basic test'

    def test_overloaded_status_code(self, app):
        """
        This test verifies that a derived class jsonifies itself correctly for
        an error handler
        """
        with app.app_context():
            client = app.test_client()
            response = client.get(flask.url_for('status'))
            assert response.status_code == 401
            response_json = json.loads(response.get_data(as_text=True))
            assert response_json['message'] == 'status test'
