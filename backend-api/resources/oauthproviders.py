from flask_restful import Resource, Api, reqparse
from flask import session, request

from oauth2client import client, crypt

from resources import google

from models.user import User
from models.trackinginfo import TrackingInfo
from models import db

import binascii
import os
import logging

api = Api

def generate_session_token():
	return binascii.hexlify(os.urandom(30))

def generate_user_account(user_dict):
	user = User(user_dict['sub'], user_dict['email'], user_dict['given_name'], user_dict['family_name'], user_dict['picture'], generate_session_token())
	db.session.add(user)

	tracking_info = TrackingInfo.generate_tracking_info(user_dict['email'])
	db.session.add(tracking_info)
			
	db.session.commit()

	return user

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
			user = generate_user_account(d)

			return user.marshal()
		

@google.tokengetter
def get_google_oauth_token():
	return session.get('google_token')

class GoogleTokenVerifier(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('idToken', type=str)
		args = parser.parse_args(strict=True)

		try:
			user_info = client.verify_id_token(args['idToken'], '346961808175-ji8aoge8npivkifclbutiu57aip6voph.apps.googleusercontent.com')
		except crypt.AppIdentityError:
			logging.info(args['idToken'])
			return {'message': 'Invalid token'}, 400

		logging.debug(user_info)

		user = User.with_gid(user_info['sub'])
		if user is None:
			user = generate_user_account(user_info)
		else:
			user.user_secret = generate_session_token()
			db.session.merge(user)
			db.session.commit()

		return user.user_secret


