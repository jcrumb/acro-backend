from resources import with_auth
from flask_restful import Resource, reqparse
from models.userlocation import UserLocation
from models import db
from datetime import datetime
from flask import request
from sqlalchemy.exc import IntegrityError
import logging

class LocationUpdateResource(Resource):
	method_decorators = [with_auth]

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('location', type=str)

		args = parser.parse_args(strict=True)
		logging.info(args)
		email = request.headers.get('x-user')

		update = UserLocation(args['location'], datetime.utcnow(), email)
		try:
			db.session.add(update)
			db.session.commit()
		except IntegrityError as e:
			logging.info(e)
			return {'error': 'error updating location'}

		return update.marshal(), 201
