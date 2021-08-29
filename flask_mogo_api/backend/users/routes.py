from flask import request, Blueprint
from backend.response import response_with
import backend.response as resp
from backend.users.models import User
import re

# creating the routes Blueprint for the templates

users = Blueprint('users', __name__)


@users.route('/register', methods=['POST'])
def register():
    """get and validate the json to have the proper data to create a new user"""

    data = request.get_json()

    """check whether the provided email is valid using regex"""

    regex = re.compile(r'''([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,4}))''', re.VERBOSE)
    mail = regex.search(data['email'])

    if mail:

        return User.create_user(first_name=data.get("first_name", None), last_name=data.get("last_name", None),
                                email=data.get("email", None), password=data.get("password", None))

    else:
        return response_with(resp.INVALID_INPUT_422, value={"msg": "invalid email"})


@users.route('/login', methods=['POST'])
def login():
    """get and validate the request json and return response with a access token(JWT token)"""
    
    data = request.get_json()

    if data.get("email", None) and data.get("password", None):

        return User.login_user(email=data["email"], password=data["password"])

    else:
        return response_with(resp.MISSING_PARAMETERS_422)
