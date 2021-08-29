from backend import create_app

# importing the create_app from the backend

app = create_app() # creating the app instance 

if __name__ == '__main__':
	# running the app
	app.run()