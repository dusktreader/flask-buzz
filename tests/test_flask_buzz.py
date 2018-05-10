import flask
import flask_buzz
import json
import pytest


class TestFlaskBuzz:

    def test_raise(self):
        with pytest.raises(flask_buzz.FlaskBuzz) as err_info:
            raise flask_buzz.FlaskBuzz('i failed')
        assert 'i failed (400)' in str(err_info.value)

    def test_jsonify__does_not_strip_headers_if_no_headers_kwarg(self, app):
        """
        This test verifies that not passing custom kwargs does not override
        the status code and headers returned by flask.jsonify.

        Addresses new functionality introduced by Flask 1.0
        """
        response = flask_buzz.FlaskBuzz('shame').jsonify()
        assert response.headers is not None
        assert response.status_code is not None

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
