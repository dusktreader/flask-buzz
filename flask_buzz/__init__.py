import buzz
import flask


class FlaskBuzz(buzz.Buzz):

    # These are the values that should be used by default when this
    # exception is handled by a flask error handler
    status_code = 400
    headers = None

    def __str__(self):
        return "{super_str} ({status_code})".format(
            super_str=super().__str__(),
            status_code=self.status_code,
        )

    def jsonify(self, status_code=None, message=None, headers=None):
        """
        Returns a representation of the error in a jsonic form that is
        compatible with flask's error handling.

        Keyword arguments allow custom error handlers to override parts of the
        exception when it is jsonified
        """
        if status_code is None:
            status_code = self.status_code
        if message is None:
            message = self.message
        if headers is None:
            headers = self.headers
        response = flask.jsonify({
            'status_code': status_code,
            'error': repr(self),
            'message': message,
        })
        if status_code is not None:
            response.status_code = status_code
        if headers is not None:
            response.headers = headers
        return response


def error_handler(error):
    """
    Supplies a generic function that may be bound to a flask error handler::

        app.register_error_handler(
            flask_buzz.FlaskBuzz, flask_buzz.error_handler,
        )
    """
    return error.jsonify()
