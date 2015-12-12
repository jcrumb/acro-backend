from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_schema():
	from os import environ as config
	from flask import Flask
	from models.user import User
	from models.usercontact import UserContact

	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = config['POSTGRES_CONN']
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)
	with app.app_context():
		db.create_all()
