from backend import mongo, bcrypt
from flask_jwt_extended import create_access_token
from backend.response import response_with
import backend.response as resp


class User:
	"""The User class defines the method for creating and logging users"""
	def find(email):
		"""return the user with the email"""
		user = mongo.db.user.find_one({"email": email})
		return user

	def create_user(first_name, last_name, email, password):
		"""To create a new user"""
		"""Check whether if all required fields are not None """
		if first_name and last_name and email and password:
			"""try to find whether any user already exist with this email"""
			user = User.find(email)

			if user:
				"""if user found with the same email return response 409 
				as a conflict with unique values in the db"""
				return response_with(resp.CONFLICT_409, value={"msg": "email already exist"})

			"""hash the password"""
			password = bcrypt.generate_password_hash(password).decode('utf-8')
			"""get the count of the user docs to keep up with the unique user _id"""
			c = mongo.db.user.count()
			"""insert the user to the mongodb"""
			id = mongo.db.user.insert_one({
							"_id": str(c+1),
							"first_name": first_name,
						        "last_name": last_name,
						        "email": email,
						        "password": password				       
						      })

			response = {
				    "first_name": first_name,
				    "last_name": last_name,
				    "email": email,
				    "password": password
				   }
			"""make response with 200 and the details of the user"""
			return response_with(resp.SUCCESS_200, value=response)

		else:
			"""if any of the parameter or field is None return 422"""
			return response_with(resp.MISSING_PARAMETERS_422)

	def login_user(email, password):
		"""To login the user by providing a jwt access token"""
		user = mongo.db.user.find_one({"email": email})
		"""find the user with the email"""
		if user and bcrypt.check_password_hash(user['password'], password):
			"""create the access token with the email as Identity"""
			access_token = create_access_token(identity=email)
			response = {
						"message": f'logged in as {user["first_name"]}',
						"access_token": access_token
						}
			"""make response with 200 and access token"""
			return response_with(resp.SUCCESS_200, value=response)

		else:
			"""if user with the requested email not found respond with 403"""
			return response_with(resp.UNAUTHORIZED_403)




