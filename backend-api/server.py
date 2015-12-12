from flask import Flask
from flask_restful import Api

from os import environ as config

from resources import oauth
from resources.oauthproviders import GoogleLoginResource, GoogleAuthResource
from resources.user import UserResource
from resources.usercontact import UserContactResource

from models import db, create_schema

create_schema()

app = Flask(__name__)
api = Api(app)

app.secret_key = config['API_SECRET_KEY']

app.config['SQLALCHEMY_DATABASE_URI']        = config['POSTGRES_CONN']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

oauth.init_app(app)
db.init_app(app)

api.add_resource(GoogleLoginResource, '/login/google')
api.add_resource(GoogleAuthResource, '/login/google/authorized', endpoint='google_authed')

api.add_resource(UserResource, '/users/<email>')
api.add_resource(UserContactResource, '/users/<email>/contacts')


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')