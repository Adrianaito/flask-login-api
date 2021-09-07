import uuid
from datetime import datetime
from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config
from Modules.DB import hash_password
from os import environ
from dotenv import load_dotenv
load_dotenv()

table = environ['SERIES']


def get_all_series_from_user(user_id, table=table):
    db_config = read_db_config()
    cnx = MySQLConnection(**db_config)
    cursor = cnx.cursor(dictionary=True, buffered=True)
    sql = f"SELECT * FROM {table} WHERE userId = '%s'" % (
        user_id)
    cursor.execute(sql)
    series = cursor.fetchall()

    cnx.commit()
    cursor.close()
    cnx.close()
    return series


def get_serie_by_id(serieId, table=table):
    db_config = read_db_config()
    cnx = MySQLConnection(**db_config)
    cursor = cnx.cursor(dictionary=True, buffered=True)

    sql = f"SELECT * FROM {table} WHERE omdbId = '%s'" % (
        serieId)
    cursor.execute(sql)
    serie = cursor.fetchone()
    id = cursor.lastrowid
    cnx.commit()
    cursor.close()
    cnx.close()

    return serie
