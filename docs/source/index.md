# flask-buzz

_py-buzz bindings specifically for Flask applications_


## Overview

This package extends the functionality from the `py-buzz` package to add some sugar for Flask apps.  `FlaskBuzz`
exception messages can be automatically jsonified with the supplied basic error handler. This means that client code can
simply register an error handler with their Flask app to supply fully prepared api responses for specific exception
types.

This means to return nicely formatted error responses when custom exceptions are raised is as simple as:

* Deriving a custom exception class from `FlaskBuzz`
* Registering the error handler with your Flask app

See [examples/basic.py](https://github.com/dusktreader/Flask-buzz/tree/main/examples/basic.py)
