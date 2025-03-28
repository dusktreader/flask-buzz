# flask-buzz

_py-buzz bindings specifically for Flask applications_


## Overview

This package extends the functionality from the `py-buzz` package to add some sugar for Flask apps.  `FlaskBuzz`
provides an exception handler builder to create nice error responses with the right status code and information included
in the response body. This means that client code can simply register an error handler with their Flask app to supply
fully prepared api responses for specific exception types.

Setting up you Flask app to return nicely formatted error responses when custom exceptions are raised is as simple as:

* Deriving a custom exception class from `FlaskBuzz`
* Registering the error handler with your Flask app

See [examples/basic.py](https://github.com/dusktreader/Flask-buzz/tree/main/examples/basic.py)
