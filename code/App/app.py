from Routes.routes import define_routes
from flask import Flask

from dotenv import load_dotenv


def prepare_api():
    load_dotenv()

    app = Flask("Login")

    return app


app = prepare_api()

# Configure Routes
define_routes(app)
