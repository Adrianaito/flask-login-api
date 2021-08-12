from typing import Union
from Modules.DB import get_user  # Change here for your case

from Helpers.Jwt import check_hashing, create_jwt


def login(user: Union[str, int], password: str = "") -> str:
    """
        TODO: Other services will also be enabled, right now just normal login will be accepted accepted!
    """
    valid_user = False
    user_data = get_user(user)
    print(user_data)

    # Let's check if user is valid! Also we need to make sure password won't get returned. this shouldn't be on client, even though it is hashed!
    if((user_data) and (check_hashing(password, user_data['password']))):
        del user_data['password']
        valid_user = True
        print("Iam here")

    token = ""
    if (valid_user):
        token = create_jwt(user_data)
        print("token", token)

    return token
