from Modules.DB import get_user
from flask_restful import Resource, request, reqparse
import requests
from os import environ
from dotenv import load_dotenv
load_dotenv()


class Omdb(Resource):

    def get(self):
        apiKey = environ["API_KEY"]
        my_payload: dict = request.get_json()
        keyword: str = my_payload.get("keyword")
        serie_id: str = my_payload.get("omdbId")
        # id example tt3896198

        if keyword:
            url = f"http://www.omdbapi.com/?t={keyword}&apikey={apiKey}"
            r = requests.get(f"{url}")
        if serie_id:
            url_id = f"http://www.omdbapi.com/?i={serie_id}&apikey={apiKey}"
            r = requests.get(f"{url_id}")

        response = r.json()
        return response
