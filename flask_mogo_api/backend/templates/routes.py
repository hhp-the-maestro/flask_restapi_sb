from flask import request,  Blueprint
from flask_jwt_extended import jwt_required
from backend.templates.models import Templates

# creating the routes Blueprint for the templates

templates = Blueprint('templates', __name__)

# The return methods used in the routes are imported from the models


@templates.route('/template', methods=['POST', 'GET'])
@jwt_required()  # jwt authentication token required
def create_get_templates():
    """if the method is GET, fetch all the templates of the current user from the db"""

    if request.method == "GET":
        current_user = Templates.get_user_and_template()
        return Templates.get_all_templates(current_user)

    """if the method is POST, get the json from the request and pass it
     to the create_template method in the Templates class in the models which in return will return a response """

    if request.method == "POST":
        data = request.get_json()

        return Templates.create_template(template_name=data.get("template_name", None),
                                subject=data.get("subject", None), body=data.get("body", None))


@templates.route('/template/<template_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required() # jwt authentication token is required
def get_update_delete_template(template_id):
    """get_user_and_template method returns the current logged in user and the requested template"""
    current_user, template = Templates.get_user_and_template(template_id)

    """for the GET method, return the template of the provided template_id"""
    if request.method == 'GET':
        return Templates.get_single_template(current_user=current_user, template=template)

    """for the PUT method, update the template of the provided template_id"""
    if request.method == 'PUT':
        data = request.get_json()

        return Templates.update_template(template_id=template_id, current_user=current_user, template=template,
                                template_name=data.get("template_name", None), subject=data.get("subject", None),
                                body=data.get("body", None))

    """for the DELETE method, delete the template of the provided template_id"""
    if request.method == 'DELETE':
        return Templates.delete_template(template_id=template_id, current_user=current_user, template=template)

