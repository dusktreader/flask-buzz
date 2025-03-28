from __future__ import annotations

from functools import partial
from http import HTTPStatus
from typing import Any, Callable, TypeAlias, cast
from typing_extensions import Self, override

import flask
from flask.typing import ResponseReturnValue, HeadersValue
from buzz import Buzz


FlaskBuzzTask: TypeAlias = Callable[["FlaskBuzz"], None]
"""A function that takes a FlaskBuzz exception and performs a task on it"""

FlaskBuzzHandler: TypeAlias = Callable[["FlaskBuzz"], ResponseReturnValue]
"""
An error handling function for flask takes an instance of `FlaskBuzz` and
returns a formatted response.
"""


class FlaskBuzz(Buzz):
    # These are the values that should be used by default when this
    # exception is handled by a flask error handler
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    headers: HeadersValue | None = None

    # If set, additional error information will be included in error
    # produced by error handlers.
    debug: bool = False

    @override
    def __str__(self):
        return "{super_str} ({status_code})".format(
            super_str=super().__str__(),
            status_code=self.status_code,
        )

    def jsonify(
        self,
        status_code: int | None = None,
        message: str | None = None,
        headers: HeadersValue | None = None,
        **kwargs: Any,
    ):
        """
        Returns a representation of the error in a jsonic form that is compatible with flask's error handling.

        Keyword arguments allow custom error handlers to override parts of the exception when it is jsonified.

        If `debug` is set, the stringified exception will be included in the response payload. For apps running in
        production or publicly should not run in debug mode as this could expose internal information to clients.

        Args:

            status_code: The status code to include in the response. If not supplied, use instance status_code.
            message:     The message to include in the response. If not supplied, use instance message. If debug
                         is set and the base_message is not None, use the base_message instead. This is important,
                         because if the exception was raised by `handle_errors`, the full message will return
                         details of the handled exception as well as the base message. This information should
                         probably not be returned to the client.
            headers:     The headers to attach to the response. If not supplied, use instance headers. If the
                         instance has no headers, don't include headers.
            kwargs:      Additional fields that should be set in the response body. These must be JSON
                         serializable.
        """
        if status_code is None:
           status_code = self.status_code
        if message is None:
            if not self.debug and self.base_message is not None:
                message = self.base_message
            else:
                message = self.message
        if headers is None and self.headers is not None:
            headers = self.headers
        else:
            headers = {}

        body: dict[str, Any] = dict(
            status_code=status_code,
            message=message,
            **kwargs,
        )

        if self.debug:
            body["error"] = str(self)
            body["headers"] = headers

        return flask.make_response(
            flask.jsonify(body),
            status_code,
            headers,
        )

    @classmethod
    def build_error_handler(cls, *tasks: FlaskBuzzTask) -> tuple[type[Self], FlaskBuzzHandler]:
        """
        Provides a generic error function that packages a flask_buzz exception so that it can be handled nicely by the
        flask error handler:

        ```python
        app.register_error_handler(FlaskBuzz, FlaskBuzz.build_error_handler())
        ```

        Additionally, extra tasks may be applied to the error prior to packaging:

        ```python
        app.register_error_handler(FlaskBuzz, build_error_handler(print, lambda e: jawa(e)))
        ```

        This latter example will print the error to stdout and also call the `jawa()` function with the error prior to
        packaging it for flask's handler
        """

        def _handler(*args: FlaskBuzzTask | Self) -> ResponseReturnValue:
            _tasks: list[FlaskBuzzTask] = [cast(FlaskBuzzTask, t) for t in args[:-1]]
            error: Self = cast(Self, args[-1])
            for task in _tasks:
                task(error)
            return error.jsonify()

        return (cls, partial(_handler, *tasks))
