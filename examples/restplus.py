import flask
import flask_buzz
import flask_restplus

app = flask.app.Flask(__name__)
api = flask_restplus.Api(app)
flask_buzz.FlaskBuzz.register_error_handler_with_flask_restplus(api)


@api.route('/index')
class MyResource(flask_restplus.Resource):

    def get(self):
        raise flask_buzz.FlaskBuzz("I died")


if __name__ == '__main__':
    app.run()
