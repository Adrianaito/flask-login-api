from Modules.DB import get_user
from API.Base import BaseResource


class Profile(BaseResource):

    def get(self):

        payload = self.check_token(0)
        print(payload)

        if not payload:
            return({'valid': False, 'message': 'Operation Not Allowed'}, 401)

        if payload:
            email = payload["email"]
            user = get_user(email)
            return user
        else:
            return ({"valid": False, "message": "Provide a valid auth token"}, 401)
