from flask_restful import Api
from flask_cors import CORS

import API as Endpoints


def define_routes(app):
    api = Api(app)
    CORS(app)

    api.add_resource(Endpoints.Auth, "/login/")
    api.add_resource(Endpoints.Register, "/register/")
    api.add_resource(Endpoints.Users, "/users/")
    api.add_resource(Endpoints.Profile, "/profile/")
