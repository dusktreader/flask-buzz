import json
import re

import flask
import flask_restx
import pytest

import flask_buzz


def stripped(text):
    """
    Removes all whitespace from a string
    """
    return re.sub(r"\s+", "", text)


class TestFlaskBuzz:
    def test_raise(self):
        with pytest.raises(flask_buzz.FlaskBuzz) as err_info:
            raise flask_buzz.FlaskBuzz("i failed")
        assert "i failed" in str(err_info.value)

    def test_jsonify__does_not_strip_headers_if_no_headers_kwarg(self, app):
        """
        This test verifies that not passing custom kwargs does not override
        the status code and headers returned by flask.jsonify.

        Addresses new functionality introduced by Flask 1.0
        """
        response = flask_buzz.FlaskBuzz("shame").jsonify()
        assert response.headers is not None
        assert response.status_code is not None

    def test_basic_functionality(self, app, capsys):
        """
        This test verifies that the basic functionality of FlaskBuzz works
        correctly. Verifies that the exception jsonifies correctly when it
        is bound to an error handler.
        """
        client = app.test_client()
        response = client.get(flask.url_for("index"))
        assert response.status_code == flask_buzz.FlaskBuzz.status_code
        response_json = json.loads(response.get_data(as_text=True))
        assert response_json["message"] == "basic test"

        (out, err) = capsys.readouterr()
        assert stripped("message: basic test") in stripped(out)

    def test_overloaded_status_code(self, app):
        """
        This test verifies that a derived class jsonifies itself correctly for
        an error handler
        """
        with app.app_context():
            client = app.test_client()
            response = client.get(flask.url_for("status"))
            assert response.status_code == 401
            response_json = json.loads(response.get_data(as_text=True))
            assert response_json["message"] == "status test"

    def test_flask_restx_error_registration(self, app, capsys):
        """
        This test verifies that registration of FlaskBuzz error handlers in
        Flask-Restx works correctly
        """
        api = flask_restx.Api(app)

        class FRPError(flask_buzz.FlaskBuzz):
            status_code = 403

        @api.route("/restx", endpoint="restx")
        class RestxResource(flask_restx.Resource):
            def get(self):
                raise FRPError("restx test")

        flask_buzz.FlaskBuzz.register_error_handler_with_flask_restx(
            api,
            lambda e: print("message: ", e.message),
            lambda e: print("status_code: ", e.status_code),
        )

        client = app.test_client()
        response = client.get(flask.url_for("restx"))
        assert response.status_code == 403
        assert response.json["message"] == "restx test"

        (out, err) = capsys.readouterr()
        assert stripped("message: restx test") in stripped(out)
