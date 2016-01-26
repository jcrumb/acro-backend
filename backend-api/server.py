from flask import Flask
from flask_restful import Api

from os import environ as config

from resources import oauth
from resources.oauthproviders import GoogleLoginResource, GoogleAuthResource, GoogleTokenVerifier
from resources.user import UserResource, UserLocationHistoryResource
from resources.usercontact import UserContactResource
from resources.locationupdate import LocationUpdateResource
from resources.tracking import TrackingInfoResource, TrackingBeginResource, TrackingEndResource, TrackingAlertResource

from models import db, create_schema
import logging

logging.basicConfig(format='%(message)s', level=logging.INFO)

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
api.add_resource(GoogleTokenVerifier, '/login/google/verifytoken')
api.add_resource(UserResource, '/users/<email>')
api.add_resource(UserContactResource, '/users/<email>/contacts')
api.add_resource(UserLocationHistoryResource, '/users/<email>/locationhistory')
api.add_resource(TrackingInfoResource, '/users/<email>/trackinginfo')

api.add_resource(TrackingBeginResource, '/tracking/begin')
api.add_resource(LocationUpdateResource, '/tracking/heartbeat')
api.add_resource(TrackingAlertResource, '/tracking/alert')
api.add_resource(TrackingEndResource, '/tracking/end')


if __name__ == '__main__':
    app.run(debug=config['API_DEBUG']=='True', port=5000, host='0.0.0.0')
