
import flask
import flask_buzz
import os
import flask_restplus

app = flask.app.Flask(__name__)
api = flask_restplus.Api(app)

ns = api.namespace("example")
api.add_namespace(ns, '/example')


class MyBaseException(flask_buzz.FlaskBuzz):
    pass


class MyException(MyBaseException):
    status_code = 418

    def __init__(self, *args, **kwargs):
        super().__init__('hard coded message', *args, **kwargs)


MyBaseException.register_error_handler_with_flask_restplus(
    api,
    lambda e: print(e),
)


def do_stuff(myvar):
    MyException.require_condition(
        myvar == 'expected',
        "didn't get 'expected' value",
    )


@ns.route('/<string:myvar>')
class MyResource(flask_restplus.Resource):

    def get(self, myvar):
        do_stuff(myvar)


if __name__ == '__main__':
    app.run(port=os.environ.get('FLASK_BUZZ_EXAMPLE_PORT', 5656))
