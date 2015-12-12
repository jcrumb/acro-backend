from flask_oauthlib.client import OAuth
from flask import request
from models.user import User
from os import environ as config

oauth = OAuth()

google = oauth.remote_app(
	'google',
	consumer_key=config['GOOGLE_CLIENT_ID'],
	consumer_secret=config['GOOGLE_CLIENT_SECRET'],
	request_token_params={
		'scope': 'email'
	},
	base_url='https://www.googleapis.com/oauth2/v1/',
	request_token_url=None,
	access_token_method='POST',
	access_token_url='https://accounts.google.com/o/oauth2/token',
	authorize_url='https://accounts.google.com/o/oauth2/auth',
	)

def with_auth(func):
	def auth_wrapper(*args, **kwargs):
		auth = request.headers.get('Authorization')
		if auth is None:
			return {'error': 'please check bearer token'}, 401

		auth = auth.split(' ')
		if len(auth) != 2:
			return {'error': 'please check bearer token'}, 401

		exists, user = User.with_token(auth[1])
		if exists is False:
			return {'error': 'please check bearer token'}, 401

		if user.user_secret != auth[1] or user.email != request.headers.get('x-user'):
			return {'error': 'please check bearer token'}, 401
		
		return func(*args, **kwargs)
	return auth_wrapper