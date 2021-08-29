from backend import mongo
from flask_jwt_extended import get_jwt_identity
from backend.response import response_with
import backend.response as resp
from flask import jsonify


class Templates:
    """The Template Class defines the methods to create, read, update and delete template"""

    def get_all_templates(current_user):
        """get all the templates from the database"""

        cursor = mongo.db.templates.find({"user_id": current_user["_id"]})
        return jsonify([doc for doc in cursor])

    def create_template(template_name, subject, body):
        """crete a new template"""
        current_user = mongo.db.user.find_one({"email": get_jwt_identity()})
        """get the current_user using the jwt token and use the user_id as a 
        relation to keep track of identifying the template author """

        user_id = current_user['_id']
        if template_name and subject and body:
            """make a new doc to keep track of the template id in the crud """
            last_id = mongo.db.template_id_track.find_one()
            last_id = last_id["last_id"]
            """insert the template in the database"""
            mongo.db.templates.insert_one({
                                        "_id": str(int(last_id)+1) ,
                                        "template_name": template_name,
                                        "subject": subject,
                                        "body": body,
                                        "user_id": user_id
                                        })

            mongo.db.template_id_track.update_one({'_id': '1'}, {"$set": {"last_id": str(int(last_id)+1)}})
            """make a response with 200 and a msg"""
            return response_with(resp.SUCCESS_200, value={"msg": "template created successfully"})
        """if any of the parameter is None we respond with 422"""
        return response_with(resp.MISSING_PARAMETERS_422, value={
            "msg": "all parameters required(template_name, subject, body)"
        })

    def get_user_and_template(template_id=None):
        """try to find the template with the given template_id and the current user"""
        
        template = mongo.db.templates.find_one({'_id': template_id})
        """find the user of the template"""
        current_user = mongo.db.user.find_one({'email': get_jwt_identity()})

        if template_id is None:
            return current_user

        return current_user, template

    def get_single_template(current_user, template):
        """return the template if the template exist"""
        if template is not None:
            if current_user['_id'] == template["user_id"]:

                return response_with(resp.SUCCESS_200, value=template)
            return response_with(resp.UNAUTHORIZED_403)

        return response_with(resp.BAD_REQUEST_400)

    def update_template(template_id, current_user, template, template_name, subject, body):
        """the update_template checks whether the provided template exist,
        if exist checks if the current user is the author of the template and update
        else respond with a unauthorized 403"""
        if template is None:
            """respond 400 if the template does not exist"""
            return response_with(resp.BAD_REQUEST_400, value={"message": "template with the given id does not exist"})

        if current_user['_id'] == template['user_id']:
            """if current user is the author of the template then update the fields which 
            are present in the request json"""
            if template_name:
                filt = {'_id': template_id}
                update = {"$set": {"template_name": template_name}}
                mongo.db.templates.update_one(filt, update)

            if subject:
                filt = {'_id': template_id}
                update = {"$set": {"subject": subject}}
                mongo.db.templates.update_one(filt, update)

            if body:
                filt = {'_id': template_id}
                update = {"$set": {"body": body}}
                mongo.db.templates.update_one(filt, update)

            return response_with(resp.SUCCESS_200, value={"msg": "template updated successfully"})
        return response_with(resp.UNAUTHORIZED_403)

    def delete_template(template_id, current_user, template):
        """If the current user is the author of the template delete the template"""

        if template is None:
            """respond 400 if the template does not exist"""
            return response_with(resp.BAD_REQUEST_400, value={"message": "template with the given id does not exist"})

        if current_user['_id'] == template["user_id"]:

            record = {"_id": template_id}

            mongo.db.templates.delete_one(record)
            return response_with(resp.SUCCESS_200, value={"msg": "template deleted successfully"})
        """return 403 if the author of the template is not the current user"""
        return response_with(resp.UNAUTHORIZED_403)
