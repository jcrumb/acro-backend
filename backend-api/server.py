from flask import Flask
from flask_restful import Api

from os import environ as config

from resources import oauth
from resources.oauthproviders import GoogleLoginResource, GoogleAuthResource

app = Flask(__name__)
api = Api(app)

oauth.init_app(app)
app.secret_key = config['API_SECRET_KEY']

api.add_resource(GoogleLoginResource, '/login/google')
api.add_resource(GoogleAuthResource, '/login/google/authorized', endpoint='google_authed')


if __name__ == '__main__':
    app.run(debug=True, port=5000)