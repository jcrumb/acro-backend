from flask_restful import Resource, Api
from flask import session, request

from resources import google

from models.user import User
from models.trackinginfo import TrackingInfo
from models import db

import binascii
import os

api = Api

class GoogleLoginResource(Resource):
	def get(self):
		return google.authorize(callback='{0}/login/google/authorized'.format(os.environ['API_BASE_URL']))

class GoogleAuthResource(Resource):
	def get(self):
		resp = google.authorized_response()
		print(resp)
		if resp is None:
			return {'message': '{0} {1}'.format(request.args['error_reason'], request.args['error_description'])}, 400


		session['google_token'] = (resp['access_token'], '')
		userinfo = google.get('userinfo')

		exists, user = User.exists(userinfo.data['email'])
		if exists:
			return user.marshal()
		else:
			d = userinfo.data
			user = User(d['email'], d['given_name'], d['family_name'], d['picture'], self.generate_token())
			db.session.add(user)

			tracking_info = TrackingInfo.generate_tracking_info(d['email'])
			db.session.add(tracking_info)
			
			db.session.commit()

			return user.marshal()

	def generate_token(self):
		return binascii.hexlify(os.urandom(30))

		

@google.tokengetter
def get_google_oauth_token():
	return session.get('google_token')
