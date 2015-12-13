from resources import with_auth
from flask_restful import Resource
from models.user import User
from models.userlocation import UserLocation

import logging

class UserResource(Resource):
	method_decorators = [with_auth]
	
	def get(self, email):
		exists, user = User.exists(email)
		if exists:
			logging.info(user)
			return user.marshal()
		else:
			return {'error': 'User does not exist'}, 404

class UserLocationHistoryResource(Resource):
	method_decorators = [with_auth]

	def get(self, email):
		exists, user = User.exists(email)
		if exists:
			locations = user.location_history[:5]
			return UserLocation.marshal_list(locations)
		else:
			return {'error': 'user not found'}, 404