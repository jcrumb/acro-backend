from resources import with_auth
from flask_restful import Resource
from models.user import User

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