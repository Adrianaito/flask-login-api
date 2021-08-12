from datetime import datetime
from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config
from Modules.DB import hash_password


def create_admin(role, email):
    date = datetime.now().strftime("%y%m%d")

    db_config = read_db_config()
    cnx = MySQLConnection(**db_config)
    cursor = cnx.cursor(dictionary=True, buffered=True)
    cursor.execute(f"""
    UPDATE USERS
    SET role=%s WHERE email=%s""",
                   (role, email))

    cnx.commit()
    cursor.close()
    cnx.close()

    return {"valid": True, "message": "Admin"}


def delete_admin(email):
    db_config = read_db_config()
    cnx = MySQLConnection(**db_config)
    cursor = cnx.cursor(dictionary=True, buffered=True)
    cursor.execute(f"""
    UPDATE USERS
    SET role=%s WHERE email=%s""",
                   (0, email))
    cnx.commit()
    cursor.close()
    cnx.close()
