Features
========

Error Codes
-----------

Each FlaskBuzz exception has a status_code class attribute. This should
correlate to the type of problem that happened. For example, the default is the
generic BAD_REQUEST (400). This just means there was a problem in the
application code itself. It is recommended to use different, informative
status codes for your different derived error classes

Flask compatible jsonify
------------------------

In order to make packaging exceptions into normal flask responses, this library
adds a ``jsonify()`` method. This method composes a flask response with the
status_code, error type, and message all embedded in a single response.

For example, your route/resource might want to raise a custom exception on
certain behaviors and have a response that informs of the error:

.. code-block:: python

   class InvalidParameters(flask_buzz.FlaskBuzz):
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
       except flask_buzz.FlaskBuzz as err:
           return err.jsonify()


Install error handler for flask
-------------------------------

The flask-buzz package also has the ability to set up a flask error handler
for FlaskBuzz exceptions. This allows any code called in the course of request
to raise a FlaskBuzz derived exception and have flask return a properly
jsonified error with status code automatically:

.. code-block:: python

   app.register_error_handler(
       flask_buzz.FlaskBuzz,
       flask_buzz.FlaskBuzz.build_error_handler(),
   )


   @app.route('/')
   def index():
       raise flask_buzz.FlaskBuzz('Nope!')

Install error handler for flask-restx
----------------------------------------

The flask-restx extension does exception handling a little bit differently.
It does not tie into the vanilla flask exception handling. Thus, you have to
do some extra things. The flask-buzz package adds some support help to register
error handlers for FlaskBuzz derived exceptions with flask-restx:

.. code-block:: python

   api = flask_restx.Api(app)
   flask_buzz.FlaskBuzz.register_error_handler_with_flask_restx(api)

   @api.route('/index')
   class MyResource(flask_restx.Resource):

       def get(self):
           raise flask_buzz.FlaskBuzz("I died")

In this example, the error handler is registered for all FlaskBuzz exceptions.
If you want to make your app only handle some custom class that's based on
FlaskBuzz, you would call the register_error_handler_with_flask_restx()
method from the derived class:

.. code-block:: python

   DerivedBuzzError.register_error_handler_with_flask_restx(api)

Adding tasks to error handlers
------------------------------

Both the regular and flask-restx error handlers support adding additional
tasks to be executed when a FlaskBuzz exception is handled. For example, you
might wish to log the exceptions before returning the response.

Each task should be a callable that takes exactly one argument: the exception
instance itself. These callables are passed as additional positional arguments:

.. code-block:: python

   def log_error(err):
       flask.current_app.logger.error(str(err))

   app.register_error_handler(
       flask_buzz.FlaskBuzz,
       flask_buzz.FlaskBuzz.build_error_handler(log_error),
   )

for flask-restx:

.. code-block:: python

   flask_buzz.FlaskBuzz.register_error_handler_with_flask_restx(
       api,
       log_error,
   )
