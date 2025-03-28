# Features

## Error Codes

Each `FlaskBuzz` exception has a `status_code` class attribute. This should correlate to the type of problem that
happened. For example, the default is the generic `INTERNAL_SERVICE_ERROR` (500). This just means there was a problem in
the application code itself. It is recommended to use different, informative status codes for your different derived
error classes.


## Flask compatible jsonify

In order to make packaging exceptions into normal Flask responses easy, this library adds a `jsonify()` method. This
method composes a Flask response with the `status_code` and the exception message included in the body (the
`status_code` is still set in the response as well)

For example, your route/resource might want to raise a custom exception on certain behaviors and have a response that
informs of the error:

```python
class InvalidParameters(FlaskBuzz):
    status_code = http.HTTPStatus.PRECONDITION_FAILED


def check_params(id=None, **params):
    if not id:
        raise InvalidParameters('id field must be defined')


@app.route('/')
def index():
    params = flask.request.args
    try:
        check_params(**params)
        return flask.jsonify(message='All good!')
    except FlaskBuzz as err:
        return err.jsonify()
```


## Install error handler for Flask

The `flask-buzz` package also has the ability to set up a Flask error handler for `FlaskBuzz exceptions`. This allows
any code called in the course of request to raise a `FlaskBuzz` derived exception and have flask return a properly
"jsonified" error response:

```python
app.register_error_handler(*FlaskBuzz.build_error_handler())


@app.route('/')
def index():
    raise FlaskBuzz('Boom!')
```

!!! note

    Notice that the unpack/splat (`*`) operator is applied to the return value of `build_error_handler`. This is because
    Flask's `register_error_handler` takes two arguments:

      * The type of exception to handle
      * A function that should be passed exception instances when they are caught

    `FlaskBuzz` returns a tuple that includes:

      * The class type that is being registered
      * A handler function to call


## Adding tasks to error handlers

`FlaskBuzz` error handlers support adding additional tasks to be executed when a `FlaskBuzz` exception is handled. For
example, you might wish to log the exceptions before returning the response.

Each task should be a callable that takes exactly one argument: the exception instance itself. These callables are
passed as additional positional arguments:

```python
def log_error(err):
    flask.current_app.logger.error(err)

app.register_error_handler(*FlaskBuzz.build_error_handler(log_error))
```


## Debug Mode

By default, the error response provided by `FlaskBuzz` error handlers include the `base_message` for the exception. This
is important only for exceptions raised by the `handle_errors()` (or `check_expressions()`) context manager. This is
because `handle_errors()` includes information about the handled error in its message. The `base_message` does not
include the full message. This is important for production/public apps where you do not wish to expose internal details
to clients.

If you want to get more information in the response to help with debugging, you can enable "Debug Mode" with `FlaskBuzz`
by setting the class property `debug` to `True`:

```python
FlaskBuzz.debug = True
```

When that flag is set, the full error message (including any handled error info) is included in the response.
Additionally, a stringified representation of the handled error is also included in the payload. Finally, when "Debug
Mode" is enabled, the response headers are also included in the body.
