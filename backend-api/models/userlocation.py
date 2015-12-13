from models import db
from flask_restful import fields, marshal

class SystemDateTime(fields.Raw):
	def format(self, value):
		return value.isoformat()

location_fields = {
	'location': fields.String,
	'datetime_utc': SystemDateTime(attribute='time'),
	'user': fields.String
}

class UserLocation(db.Model):
	__tablename__ = 'location_history'
	user          = db.Column(db.String, db.ForeignKey('users.email'), primary_key=True)
	location      = db.Column(db.String)
	time          = db.Column(db.DateTime, primary_key=True)

	def __init__(self, location, time, email):
		self.location = location
		self.user     = email
		self.time     = time

	def marshal(self):
		return marshal(self, location_fields)

	@staticmethod
	def marshal_list(locations):
		return marshal(locations, location_fields)