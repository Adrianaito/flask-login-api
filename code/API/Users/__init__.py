from mysql.connector.errors import IntegrityError
from Modules.DB import create_admin, delete_admin
from flask_restful import Resource, request, reqparse
from Modules.DB import delete_from_db
from Modules.DB import get_user, update_users_db, get_all_users
from Helpers.Jwt import validate_jwt
from flask import jsonify, make_response


class Users(Resource):

    def get(self):

        auth_header: dict = request.headers.get('Authorization')

        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = validate_jwt(auth_token)
            valid = resp["jwt_valid"]
            if valid:
                users = get_all_users()
            return users
        else:

            return ({"valid": False, "message": "Provide a valid auth token"}, 401)

    def put(self):

        auth_header: dict = request.headers.get('Authorization')

        my_payload: dict = request.get_json()
        email: str = my_payload["email"]
        delete: bool = my_payload["delete"]

        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        resp = validate_jwt(auth_token)
        valid = resp["jwt_valid"]
        if valid:
            user = get_user(email)
            if not user:
                return ({"valid": False, "message": "user not found"})
            if not delete:
                role = 1
                create_admin(role, email)
                return ({"admin": True, "message": "admin created", "valid": True}, 200)
            if delete:
                delete_admin(email)
                return ({"message": "admin removed", "valid": True, "admin": False}, 200)
        else:

            return ({"valid": False, "message": "Provide a valid auth token"}, 401)

    def patch(self):

        auth_header: dict = request.headers.get('Authorization')

        my_payload: dict = request.get_json()
        name: str = my_payload["name"]
        email: str = my_payload["email"]
        id: str = my_payload["public_id"]

        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        resp = validate_jwt(auth_token)
        valid = resp["jwt_valid"]

        if valid:

            update_users_db(id, name, email)

            return ({"valid": True, "message": "Updated user successfully!"}, 200)
        else:

            return ({"valid": False, "message": "Provide a valid auth token"}, 401)

    def delete(self):

        auth_header: dict = request.headers.get('Authorization')

        my_payload: dict = request.get_json()
        data_id: str = my_payload["id"]
        table: str = my_payload["table"]

        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        resp = validate_jwt(auth_token)
        valid = resp["jwt_valid"]

        if valid:
            delete_from_db(data_id, table)
            return ({
                "valid": True,
                "message": "Successfully deleted"
            }, 200)
        else:
            return ({"valid": False, "message": "Provide a valid auth token"}, 401)
