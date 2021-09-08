import uuid
from datetime import datetime
from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config
from Modules.DB import hash_password
from os import environ
from dotenv import load_dotenv
load_dotenv()

table = environ['USERS']


def get_user(email, table=table):
    db_config = read_db_config()
    cnx = MySQLConnection(**db_config)
    cursor = cnx.cursor(dictionary=True, buffered=True)
    sql = f"SELECT email, password, role, public_id, id FROM {table} WHERE email = '%s'" % (
        email)
    cursor.execute(sql)
    user = cursor.fetchone()

    cnx.commit()
    cursor.close()
    cnx.close()
    return user


def get_all_users(table=table):
    db_config = read_db_config()
    cnx = MySQLConnection(**db_config)
    cursor = cnx.cursor(dictionary=True, buffered=True)
    sql = f"SELECT name, role, public_id FROM {table} "
    cursor.execute(sql)
    users = cursor.fetchall()

    cnx.commit()
    cursor.close()
    cnx.close()
    return users


def create_user(email, password, table=table):
    """
        Creates a new user in the database
        Fields that are needed here:  email, password
    """
    date = datetime.now().strftime("%Y%m%d")
    hashed_password = hash_password(password)
    uid = uuid.uuid4()
    id_s = str(uid)
    id = id_s[:10]
    role = 0

    db_config = read_db_config()
    cnx = MySQLConnection(**db_config)
    cursor = cnx.cursor(dictionary=True, buffered=True)
    sql_query = (f"INSERT INTO {table} (role, email, password, public_id)"
                 "VALUES (%s, %s, %s, %s)")
    data = (role, email, hashed_password, id)

    cursor.execute(sql_query, tuple(data))
    user_id = cursor.lastrowid
    # Commit transaction
    cnx.commit()
    cursor.close()
    cnx.close()

    return id


def update_users_db(id, name="", email="", table=table):
    db_config = read_db_config()
    cnx = MySQLConnection(**db_config)
    cursor = cnx.cursor(dictionary=True, buffered=True)

    cursor.execute(f"""
    UPDATE {table}
    SET name=%s, email=%s WHERE public_id=%s""",
                   (name, email, id))

    cnx.commit()
    cursor.close()
    cnx.close()
    return ({"valid": True})
