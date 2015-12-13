from models import db
from flask_restful import fields, marshal

user_fields = {
	'email': fields.String,
	'firstName': fields.String(attribute='first_name'),
	'lastName': fields.String(attribute='last_name'),
	'picture': fields.String(attribute='profile_picture_url'),
	'token': fields.String(attribute='user_secret')
}

class User(db.Model):
	__tablename__       = 'users'
	email               = db.Column(db.String, primary_key=True)
	first_name          = db.Column(db.String)
	last_name           = db.Column(db.String)
	user_secret         = db.Column(db.String)
	profile_picture_url = db.Column(db.String)
	contacts            = db.relationship('UserContact')
	location_history    = db.relationship('UserLocation', order_by='desc(UserLocation.time)')

	def __init__(self, email, first, last, picture, secret):
		self.email               = email
		self.first_name          = first
		self.last_name           = last
		self.profile_picture_url = picture
		self.user_secret         = secret

	def __repr__(self):
		return 'First: {0} Last: {1} Email: {2}'.format(self.first_name, self.last_name, self.email)

	def marshal(self):
		return marshal(self, user_fields)

	@staticmethod
	def exists(email):
		user = db.session.query(User).filter(User.email == email).one_or_none()

		if user is None:
			return False, None
		else:
			return True, user

	@staticmethod
	def with_token(token):
		user = db.session.query(User).filter(User.user_secret == token).one_or_none()

		if user is None:
			return False, None
		else:
			return True, user

	@staticmethod
	def with_email(email):
		exists, user = User.exists(email)
		if exists == False:
			raise Exception('No user found')
		return user