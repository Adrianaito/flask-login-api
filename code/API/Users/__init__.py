from Modules.DB.AdminDb import create_admin, delete_admin
from flask_restful import request
from Modules.DB import get_user, update_users_db, get_all_users, delete_from_db
from API.Base import BaseResource


class Users(BaseResource):

    def get(self):

        payload = self.check_token()

        if not payload:
            return({'valid': False, 'message': 'Operation Not Allowed'}, 401)
        else:
            users = get_all_users()
            return users

    def put(self):

        payload = self.check_token(1)

        my_payload: dict = request.get_json()
        email: str = my_payload["email"]
        delete: bool = my_payload["delete"]

        if not payload:
            return({'valid': False, 'message': 'Operation Not Allowed'}, 401)
        else:
            user = get_user(email)
            if not user:
                return ({"valid": False, "message": "user not found"})
            if not delete:
                role = 1
                create_admin(role, email)
                return ({"admin": True, "message": "admin created", "valid": True}, 200)
            if delete:
                delete_admin(email)
                return ({"message": "admin removed", "valid": True, "admin": False}, 200)

    def patch(self):

        payload = self.check_token(1)

        if not payload:
            return({'valid': False, 'message': 'Operation Not Allowed'}, 401)

        my_payload: dict = request.get_json()
        name: str = my_payload["name"]
        email: str = my_payload["email"]
        id: str = my_payload["public_id"]

        user = update_users_db(id, name, email)

        return ({"valid": True, "message": "Updated user successfully!"}, 200)

    def delete(self):

        payload = self.check_token(1)

        if not payload:
            return({'valid': False, 'message': 'Operation Not Allowed'}, 401)

        my_payload: dict = request.get_json()
        data_id: str = my_payload["id"]
        table: str = my_payload["table"]

        delete_from_db(data_id, table)
        return ({
            "valid": True,
            "message": "Successfully deleted"
        }, 200)
