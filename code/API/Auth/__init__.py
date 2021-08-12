from mysql.connector.errors import IntegrityError
from flask_restful import Resource, request, reqparse
from flask import jsonify
from Modules.Auth import login


class Auth(Resource):

    def post(self):

        my_payload: dict = request.get_json()
        email: str = my_payload.get("email")
        password: str = my_payload.get("password")

        print(email)
        data = request.get_json()
        if not data:
            return ({"valid": False, "message": "Invalid Request", "token": None}, 403)

        jwt = login(email, password)
        print(jwt)
        if not jwt:
            return ({"valid": False, "message": "Could not Log User", "token": None}, 404)

        return ({"valid": True, "message": "Log in Successfull", "token": jwt}, 200)
