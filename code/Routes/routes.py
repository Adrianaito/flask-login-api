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
    # api.add_resource(Endpoints.Pdf, "/pdf/")
    # api.add_resource(Endpoints.FileScan, "/file/")
    # api.add_resource(Endpoints.SortingUnit, "/sortingRule/")
    # api.add_resource(Endpoints.Password, "/resetPassword/")
    # api.add_resource(Endpoints.Today, "/today/")
    # api.add_resource(Endpoints.Search,
    #                  "/search/<string:field>/<string:value>/")
    # api.add_resource(Endpoints.SearchUser,
    #                  "/searchUser/")

    # api.add_resource(Print.Print, "/print")
