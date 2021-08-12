import bcrypt
from jwt import encode, decode
from jwt import ExpiredSignatureError, InvalidSignatureError
from datetime import timedelta, datetime
from dotenv import load_dotenv
from os import environ
import logging

load_dotenv()

JWT_STATUS_VALID = -1
JWT_ERROR = 0
JWT_STATUS_INVALID_SIGNATURE = 1
JWT_STATUS_EXPIRED_JWT = 2


def create_jwt(payload: dict, algorithm: str = "HS256", time_valid: int = 12):
    jwt_secret = environ["JWT_KEY"]

    # Add validation specific rules to jwt
    payload["expiration"] = (
        datetime.utcnow() + timedelta(hours=time_valid)).strftime("%Y-%m-%d %H:%M:%S")

    jwt_str = encode(payload, jwt_secret, algorithm=algorithm)
    return jwt_str


def validate_jwt(jwt_str: str, algorithm: str = "HS256"):
    log = logging.getLogger("JWT - Validate")
    jwt_secret = environ["JWT_KEY"]

    try:
        payload = decode(jwt_str, jwt_secret, algorithms=algorithm)
    except InvalidSignatureError as e:
        log.exception(e)
        return return_jwt_verified(jwt_status=JWT_STATUS_INVALID_SIGNATURE)
    except ExpiredSignatureError as e:
        log.exception(e)
        return return_jwt_verified(jwt_status=JWT_STATUS_EXPIRED_JWT)
    except Exception as e:
        log.exception(e)
        return return_jwt_verified(jwt_status=JWT_ERROR)

    return return_jwt_verified(jwt_payload=payload, jwt_status=JWT_STATUS_VALID)


def return_jwt_verified(jwt_payload: dict = {}, jwt_status: int = JWT_ERROR):
    return {
        "payload": jwt_payload,
        "status": jwt_status,
        "jwt_valid": (jwt_status < 0),
    }


def create_hashed(value: str):
    """
        Hashes a string using bcrypt hashing algorithm
    """
    binary_value = value.encode()
    salt = bcrypt.gensalt()
    hashed_value = bcrypt.hashpw(binary_value, salt)

    return hashed_value


def check_hashing(value: str, hashed_value: str):
    """
        Checks the hashed value to guarantee it matches
    """
    status = False

    try:
        status = bcrypt.checkpw(
            value.encode(),
            hashed_value.encode()
        )
    except ValueError as e:
        if not (str(e) == "Invalid salt"):
            raise e

    return status
