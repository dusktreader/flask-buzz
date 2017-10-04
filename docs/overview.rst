Overview
========

This package extends the functionality from the py-buzz package to add some
sugar for flask apps.  FlaskBuzz exception messages can be automatically
jsonified with the supplied basic error handler. This means that client code
can simply register an error handler with their flask app to supply fully
prepared api responses for specific excpetion types.

This means returning responses when custom exceptions are raised in your flask
app are as simple as::

* Derive a custom exception class from FlaskBuzz
* Register the error handler with your flask app

See `examples/basic.py
<https://github.com/dusktreader/flask-buzz/tree/master/examples/basic.py>`_
