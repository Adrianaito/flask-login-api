from Modules.DB import get_user
from flask_restful import Resource, request, reqparse
import requests
from os import environ
from dotenv import load_dotenv
load_dotenv()


class Search(Resource):

    def post(self):
        apiKey = environ["API_KEY"]
        my_payload: dict = request.get_json()
        data = my_payload.get("data")
        keyword: str = data.get("keyword")
        serie_id: str = my_payload.get("omdbId")
        # id example tt3896198
        print("search payload", my_payload)
        print(keyword)
        if keyword:
            url = f"http://www.omdbapi.com/?t={keyword}&apikey={apiKey}"
            r = requests.get(f"{url}")
        if serie_id:
            url_id = f"http://www.omdbapi.com/?i={serie_id}&apikey={apiKey}"
            r = requests.get(f"{url_id}")

        response = r.json()
        return response
