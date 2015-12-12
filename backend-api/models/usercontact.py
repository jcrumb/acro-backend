from models import db
from flask_restful import fields, marshal

contact_fields = {
	'phoneNumber': fields.String(attribute='phone_number'),
	'firstName': fields.String(attribute='first_name'),
	'lastName': fields.String(attribute='last_name')
}

class UserContact(db.Model):
	__tablename__ = 'user_contacts'
	phone_number  = db.Column(db.String, primary_key=True)
	user          = db.Column(db.String, db.ForeignKey('users.email'), primary_key=True)
	first_name    = db.Column(db.String)
	last_name     = db.Column(db.String)

	def __init__(self, email, first, last, phone):
		self.user         = email
		self.first_name   = first
		self.last_name    = last
		self.phone_number = phone

	def marshal(self):
		return marshal(self, contact_fields)
