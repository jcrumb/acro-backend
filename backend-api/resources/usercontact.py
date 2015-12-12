from resources import with_auth
from flask_restful import Resource, reqparse
from models.usercontact import UserContact, contact_fields
from sqlalchemy.orm.exc import NoResultFound
from flask_restful import marshal
from models.user import User
from models import db
from sqlalchemy.exc import IntegrityError

class UserContactResource(Resource):
	method_decorators = [with_auth]

	def get(self, email):
		user = User.with_email(email)

		return marshal(user.contacts, contact_fields)

	def post(self, email):
		parser = reqparse.RequestParser()
		parser.add_argument('firstName', type=str)
		parser.add_argument('lastName', type=str)
		parser.add_argument('phoneNumber', type=str)

		args = parser.parse_args(strict=True)
		contact = UserContact(email, args['firstName'], args['lastName'], args['phoneNumber'])
		db.session.add(contact)
		try:
			db.session.commit()
		except IntegrityError as e:
			return {'error': 'Contact already exists for user'}, 400

		return contact.marshal(), 201

	def delete(self, email):
		parser = reqparse.RequestParser()
		parser.add_argument('phoneNumber', type=str)

		args = parser.parse_args(strict=True)

		try:
			contact = (db.session.query(UserContact)
			.filter(UserContact.phone_number == args['phoneNumber'])
			.filter(UserContact.user == email).one())
		except NoResultFound:
			return {'error': 'No contact found, please check number'}, 404

		db.session.delete(contact)
		db.session.commit()
		return {'message': 'contact deleted'}
