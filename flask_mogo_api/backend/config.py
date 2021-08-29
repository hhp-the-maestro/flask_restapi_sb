import os

# As the secret keys are stored as environment variables we'll get them using the os module

class Config:
	JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
	MONGO_URI = os.environ.get("MONGO_URI")
	