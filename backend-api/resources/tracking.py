from resources import with_auth, cache, twilio_client
from models import db
from flask_restful import Resource, reqparse
from models.trackinginfo import TrackingInfo
from flask import request
from datetime import datetime
from models.user import User
from os import environ as config
import pickle
import logging

HOUR = 3600

class TrackingInfoResource(Resource):
	method_decorators = [with_auth]

	def get(self, email):
		tracking_info = db.session.query(TrackingInfo).filter(TrackingInfo.user == email).one()
		return tracking_info.marshal()

class TrackingBeginResource(Resource):
	method_decorators = [with_auth]

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('location', type=str)

		args           = parser.parse_args(strict=True)
		tracking_status = {}

		user = User.with_email(request.headers.get('X-User'))

		tracking_status['tracking_pin'] = user.tracking_info.tracking_pin
		tracking_status['location']     = args['location']
		tracking_status['timestamp']    = datetime.utcnow().isoformat()
		tracking_status['photo_url']    = user.profile_picture_url
		tracking_status['status']       = 'active'
		tracking_status['first_name']   = user.first_name
		tracking_status['last_name']    = user.last_name

		tracking_pickle = pickle.dumps(tracking_status)
		logging.info(tracking_pickle)

		cache.setex('tracking:' + user.tracking_info.tracking_id, HOUR * 1, tracking_pickle)

		return user.tracking_info.marshal()

class TrackingEndResource(Resource):
	method_decorators = [with_auth]

	def get(self):
		user = User.with_email(request.headers.get('X-User'))

		cache.delete('tracking:' + user.tracking_info.tracking_id)
		return {'message': 'tracking stopped'}

class TrackingAlertResource(Resource):
	method_decorators = [with_auth]

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('location', type=str, required=False)

		args = parser.parse_args(strict=True)
		user = User.with_email(request.headers.get('X-User'))

		tracking_status = cache.get('tracking:'+user.tracking_info.tracking_id)
		ts = pickle.loads(tracking_status)
		if args['location'] != None:
			ts['location']      = args['location']
			ts['timestamp']     = datetime.utcnow().isoformat()
			ts['location_type'] = 'current'
		else:
			ts['location_type'] = 'last_known'

		ts['status'] = 'alert'

		tracking_status = pickle.dumps(ts)
		cache.setex('tracking:'+user.tracking_info.tracking_id, HOUR * 12, tracking_status)

		message = ('An alert has been generated for {0} {1}, '
		          'please go to {2} to view their location and status using PIN {3}.'
		          ' This link will remain active for 12 hours.'.format(
		          	user.first_name, user.last_name, user.tracking_info.tracking_url(),
		          	user.tracking_info.tracking_pin))

		for number in [c.phone_number for c in user.contacts]:
			logging.info('Sending message to {0} for {1}'.format(number, user.tracking_info.tracking_id))
			twilio_client.messages.create(
				to=number,
				from_=config['TWILIO_OUTGOING_NUM'],
				body=message
				)

		return {'message': 'alerts sent successfully'}