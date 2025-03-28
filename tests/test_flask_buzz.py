import json
import re
from typing import Any

import flask
import pytest

from flask_buzz import FlaskBuzz


def stripped(text: str):
    """
    Removes all whitespace from a string
    """
    return re.sub(r"\s+", "", text)


class TestFlaskBuzz:

    def test_raise(self):
        with pytest.raises(FlaskBuzz) as err_info:
            raise FlaskBuzz("i failed")
        assert "i failed" in str(err_info.value)

    @pytest.mark.usefixtures("app")
    def test_jsonify__does_not_strip_headers_if_no_headers_kwarg(self):
        """
        This test verifies that not passing custom kwargs does not override
        the status code and headers returned by flask.jsonify.

        Addresses new functionality introduced by Flask 1.0
        """
        response = FlaskBuzz("shame").jsonify()
        assert response.headers is not None
        assert response.status_code is not None

    def test_basic_functionality(self, app: flask.Flask):
        """
        This test verifies that the basic functionality of FlaskBuzz works
        correctly. Verifies that the exception jsonifies correctly when it
        is bound to an error handler.
        """

        calls: list[tuple[str, Exception]] = []
        def task1(err: Exception):
            calls.append(("task1", err))

        def task2(err: Exception):
            calls.append(("task2", err))

        app.register_error_handler(*FlaskBuzz.build_error_handler(task1, task2))

        client = app.test_client()
        response = client.get(flask.url_for("index"))
        assert response.status_code == FlaskBuzz.status_code
        response_json: dict[str, Any] | None = response.json
        assert response_json is not None
        assert response_json["message"] == "basic test"
        assert response_json["status_code"] == FlaskBuzz.status_code
        assert [c[0] for c in calls] == ["task1", "task2"]

    def test_debug_mode(self, app: flask.Flask):
        """
        This test verifies that FlaskBuzz includes error information and uses
        the `base_message` in the response payload when running in debug mode.
        correctly. Verifies that the exception jsonifies correctly when it
        is bound to an error handler.
        """
        app.register_error_handler(*FlaskBuzz.build_error_handler())
        client = app.test_client()

        response = client.get(flask.url_for("dangerous"))
        assert response.status_code == FlaskBuzz.status_code
        safe_response_json: dict[str, Any] | None = response.json
        assert safe_response_json is not None
        assert safe_response_json["message"] == "base message"
        assert "dangerous test" not in safe_response_json["message"]
        assert safe_response_json["status_code"] == FlaskBuzz.status_code

        try:
            FlaskBuzz.debug = True
            response = client.get(flask.url_for("dangerous"))
            pass
        finally:
            FlaskBuzz.debug = False

        assert response.status_code == FlaskBuzz.status_code
        debug_response_jason: dict[str, Any] | None = response.json
        assert debug_response_jason is not None
        assert debug_response_jason["message"] != "base message"
        assert "base message" in debug_response_jason["message"]
        assert "dangerous test" in debug_response_jason["message"]
        assert debug_response_jason["status_code"] == FlaskBuzz.status_code

    def test_overloaded_status_code(self, app: flask.Flask):
        """
        This test verifies that a derived class jsonifies itself correctly for
        an error handler.
        """
        app.register_error_handler(*FlaskBuzz.build_error_handler())

        with app.app_context():
            client = app.test_client()
            response = client.get(flask.url_for("status"))
            assert response.status_code == 401
            response_json = json.loads(response.get_data(as_text=True))
            assert response_json["message"] == "status test"
