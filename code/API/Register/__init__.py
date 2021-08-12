from mysql.connector.errors import IntegrityError
from flask_restful import Resource, request, reqparse
from Modules.DB import create_user


class Register(Resource):

    def post(self):

        my_payload: dict = request.get_json()
        email: str = my_payload.get("email")
        password: str = my_payload.get("password")

        if not email or not password:
            return ({"valid": False, "message": "Missing required fields"})

        try:
            account = create_user(email, password)

            return ({
                "valid": True,
                "Message": "New user saved",
                "admin": False,
                "id": account
            }, 200)
        except IntegrityError as error:
            return({"valid": False, "message": error.msg, "duplicated": True})
