import inspect
import flask
import pytest

from flask_buzz import FlaskBuzz


class OverloadBuzz(FlaskBuzz):
    status_code: int = 401


def func_name() -> str:
    frame = inspect.currentframe()
    assert frame is not None
    return frame.f_code.co_name


@pytest.fixture
def app():
    app = flask.Flask("normal_app")
    app.debug = False
    app.config["TESTING"] = True
    app.config["SERVER_NAME"] = "test_server"

    @app.route("/")
    def index():  # pyright: ignore[reportUnusedFunction]
        raise FlaskBuzz("basic test")

    @app.route("/status")
    def status():  # pyright: ignore[reportUnusedFunction]
        raise OverloadBuzz("status test")

    @app.route("/dangerous")
    def dangerous():  # pyright: ignore[reportUnusedFunction]
        with FlaskBuzz.handle_errors("base message"):
            raise RuntimeError("dangerous test")

    @app.route("/unhandled")
    def unhandled():  # pyright: ignore[reportUnusedFunction]
        raise RuntimeError("unhandled test")

    with app.app_context():
        yield app
