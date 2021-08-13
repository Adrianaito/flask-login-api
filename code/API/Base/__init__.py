from flask import request
from flask_restful import Resource

from Helpers.Jwt import validate_jwt


class BaseResource(Resource):

    def check_token(self, minimum_role: int = 0) -> dict:
        # JWT verification!
        payload = request.headers.get('Authorization', None)

        if payload == None:
            return{}

        token = payload.split(' ')[1]
        status = validate_jwt(token)

        if (not status['jwt_valid']):
            return {}

        if(int(status['payload']['role']) >= minimum_role):
            return status['payload']


# class BaseResource(Resource):

#     def check_token(self, minimum_role: int = 0) -> dict:
#         # JWT verification!
#         token = request.headers.get('Authorization', None).split(' ')[1]
#         status = validate_jwt(token)
#         if (not status['jwt_valid']):
#             return {}

#         if(int(status['payload']['role']) >= minimum_role):
#             # return {}

#             return status['payload']
