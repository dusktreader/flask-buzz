import flask
import flask_buzz
import flask_restx

app = flask.app.Flask(__name__)
api = flask_restx.Api(app)
flask_buzz.FlaskBuzz.register_error_handler_with_flask_restx(api)


@api.route('/index')
class MyResource(flask_restx.Resource):

    def get(self):
        raise flask_buzz.FlaskBuzz("I died")


if __name__ == '__main__':
    app.run()
