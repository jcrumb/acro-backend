from resources import with_auth, cache
from flask_restful import Resource, reqparse
from models.user import User
from models.userlocation import UserLocation
from models import db
from datetime import datetime
from flask import request
from sqlalchemy.exc import IntegrityError
import pickle
import logging

HOUR = 3600

class LocationUpdateResource(Resource):
	method_decorators = [with_auth]

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('location', type=str)

		args = parser.parse_args(strict=True)
		logging.info(args)
		email = request.headers.get('X-User')

		update = UserLocation(args['location'], datetime.utcnow(), email)
		try:
			db.session.add(update)
			db.session.commit()
		except IntegrityError as e:
			logging.info(e)
			return {'error': 'error updating location'}

		# Update tracking info in cache as well
		t = User.with_email(email).tracking_info
		tracking_status = cache.get('tracking:'+t.tracking_id)
		if tracking_status != None:
			tm = pickle.loads(tracking_status)
			tm['location'] = args['location']
			tm['timestamp'] = datetime.utcnow().isoformat()

			tracking_status = pickle.dumps(tm)
			cache.setex('tracking:'+t.tracking_id, HOUR * 1, tracking_status)

		return update.marshal(), 201
