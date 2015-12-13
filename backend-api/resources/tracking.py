from resources import with_auth
from models import db
from flask_restful import Resource
from models.trackinginfo import TrackingInfo

import logging

class TrackingInfoResource(Resource):
	method_decorators = [with_auth]

	def get(self, email):
		tracking_info = db.session.query(TrackingInfo).filter(TrackingInfo.user == email).one()
		return tracking_info.marshal()
