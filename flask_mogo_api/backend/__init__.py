from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from backend.config import Config


mongo = PyMongo()
bcrypt = Bcrypt()
jwt = JWTManager()


# Instantiating and Binding the flask app

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	mongo.init_app(app)     # creating database instance of the app
	bcrypt.init_app(app)  	# Instantiating  bcrypt for hashing passwords
	jwt.init_app(app)		# JWT token manager instance of the app

	from backend.users.routes import users    # importing the user routes from the users module
	from backend.templates.routes import templates	  # importing the templates route from the templates module

# Registering the users and templates route

	app.register_blueprint(users)
	app.register_blueprint(templates)

	return app


