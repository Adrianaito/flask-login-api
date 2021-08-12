from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config
from Helpers.Jwt import create_hashed
from os import environ
from dotenv import load_dotenv
load_dotenv()


table = environ["USERS"]


def hash_password(raw_password: str) -> str:

    return create_hashed(raw_password)


def reset_password(password, email, table=table):
    db_config = read_db_config()
    cnx = MySQLConnection(**db_config)
    cursor = cnx.cursor(dictionary=True, buffered=True)
    hashed_password = hash_password(password)

    cursor.execute(f"""
    UPDATE {table}
    SET password=%s WHERE email=%s""",
                   (hashed_password, email))
    cnx.commit()
    cursor.close()
    cnx.close()
