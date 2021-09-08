from mysql.connector.errors import IntegrityError
from API.Base import BaseResource
from flask_restful import Resource, request, reqparse
from Modules.DB.SeriesDb import save_serie
from Modules.DB.SeriesDb import get_serie_by_id, get_all_series_from_user


class Series(BaseResource):

    def get(self):

        payload = self.check_token(0)
        print(payload)

        if not payload:
            return({'valid': False, 'message': 'Operation Not Allowed'}, 401)

        if payload:
            user_id = payload["id"]
            series = get_all_series_from_user(user_id)
            return series
        else:
            return ({"valid": False, "message": "Provide a valid auth token"}, 401)

    def post(self):

        payload = self.check_token(0)
        print(payload)
        my_payload: dict = request.get_json()
        print("my payload", my_payload)
        data = my_payload.get("data")
        title = data.get("title")
        year = data.get("year")
        released = data.get("released")
        genre = data.get("genre")
        country = data.get("country")
        poster = data.get("poster")
        imdbRating = data.get("imdbRating")
        imdbId = data.get("imdbId")
        type = data.get("type")
        totalSeasons = data.get("totalSeasons")

        if not payload:
            return({'valid': False, 'message': 'Operation Not Allowed'}, 401)

        if payload:
            user_id = payload["id"]
            try:
                serie_id = save_serie(title, year, released, genre, country,
                                      poster, imdbRating, imdbId, type, totalSeasons, user_id)
                return serie_id
            except IntegrityError as e:
                return ({"message": "duplicated", "vallid": False})
        else:
            return ({"valid": False, "message": "Provide a valid auth token"}, 401)
