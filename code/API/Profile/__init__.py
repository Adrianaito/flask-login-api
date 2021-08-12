from mysql.connector.errors import IntegrityError
from Modules.DB import create_admin, delete_admin
from flask_restful import Resource, request, reqparse
from Modules.DB import delete_from_db
from Modules.DB import get_user, update_users_db, get_all_users
from Helpers.Jwt import validate_jwt
from flask import jsonify, make_response


class Profile(Resource):

    def get(self):

        auth_header: dict = request.headers.get('Authorization')

        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = validate_jwt(auth_token)
            payload = resp["payload"]
            if payload:
                email = payload["email"]
                user = get_user(email)
                return user
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401
