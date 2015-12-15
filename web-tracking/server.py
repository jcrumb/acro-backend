from flask import render_template, Flask, redirect, jsonify
from flask_restful import reqparse
import redis
from os import environ as config
import pickle

app = Flask(__name__)

cache = redis.StrictRedis(host=config['REDIS_HOST'], port=int(config['REDIS_PORT']), db=0)

@app.route('/tracking/<tracking_id>/', methods=['GET'])
def serve_tracking_page(tracking_id):
	context = {}
	context['tracking_id'] = tracking_id

	if cache.exists('tracking:'+tracking_id):
		return render_template('track.html', **context)
	else:
		return redirect('/static/inactive.html')

@app.route('/tracking/pin/verify/', methods=['POST'])
def verify_pin():
		parser = reqparse.RequestParser()
		parser.add_argument('trackingId', type=str)
		parser.add_argument('pin', type=str)

		args = parser.parse_args(strict=True)

		t = cache.get('tracking:'+args['trackingId'])
		if t == None:
			return jsonify(error='Tracking ID inactive'), 400

		info = pickle.loads(t)
		if info['tracking_pin'] != args['pin']:
			return jsonify(error='Tracking ID inactive'), 400

		info.pop('tracking_pin', None)
		return jsonify(**info)



if __name__ == '__main__':
	app.run(debug=config['DEBUG']=='True', port=5001, host='0.0.0.0')
