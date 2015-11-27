from flask_restful import Resource, Api
from flask import jsonify, session, current_app

from resources import google

api = Api

class GoogleLoginResource(Resource):
	def get(self):
		return google.authorize(callback=api.url_for(api(current_app), GoogleAuthResource, _external=True))

class GoogleAuthResource(Resource):
	def get(self):
		resp = google.authorized_response()
		print(resp)
		if resp is None:
			return {'message': 'You fail'}
		session['google_token'] = (resp['access_token'], '')
		me = google.get('userinfo')
		return jsonify({'data': me.data})


@google.tokengetter
def get_google_oauth_token():
	return session.get('google_token')