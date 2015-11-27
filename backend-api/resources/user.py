from resources import with_auth
from flask_restful import Resource
from models.user import User


class UserResource(Resource):
	method_decorators = [with_auth]
	
	def get(self, email):
		exists, user = User.exists(email)
		if exists:
			return user.marshal()
		else:
			return {'error': 'User does not exist'}, 404