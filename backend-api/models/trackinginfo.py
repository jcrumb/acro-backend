from models import db
from flask_restful import fields, marshal
import random
import datetime
import string

def generate_tracking_id():
	random.seed(datetime.datetime.utcnow())
	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in xrange(6))

def generate_tracking_pin():
	random.seed(datetime.datetime.utcnow())
	return ''.join(random.choice(string.digits) for _ in xrange(4))

class UrlGenerator(fields.Raw):
	def format(self, value):
		return 'https://www.getacro.com/tracking/{0}'.format(value)

tracking_fields = {
	'trackingId': fields.String(attribute='tracking_id'),
	'trackingUrl': UrlGenerator(attribute='tracking_id'),
	'trackingPin': fields.String(attribute='tracking_pin')
}

class TrackingInfo(db.Model):
	__tablename__ = 'tracking_info'
	user          = db.Column(db.String, db.ForeignKey('users.email'), nullable=False)
	tracking_id   = db.Column(db.String, primary_key=True)
	tracking_pin  = db.Column(db.String, nullable=False)

	def __init__(self, email, id, pin):
		self.user         = email
		self.tracking_id  = id
		self.tracking_pin = pin

	def marshal(self):
		return marshal(self, tracking_fields)

	def tracking_url(self):
		return UrlGenerator().format(self.tracking_id)

	@staticmethod
	def generate_tracking_info(email):
		tracking_id = generate_tracking_id()
		while db.session.query(TrackingInfo).filter(TrackingInfo.tracking_id == tracking_id).one_or_none() != None:
			tracking_id = generate_tracking_id()
		tracking_info = TrackingInfo(email, tracking_id, generate_tracking_pin())

		return tracking_info