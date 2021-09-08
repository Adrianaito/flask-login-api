import uuid
from datetime import datetime
from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config
from Modules.DB import hash_password
from os import environ
from dotenv import load_dotenv
load_dotenv()

table = environ['SERIES']


def save_serie(title: str,
               year: str,
               released: str,
               genre: str,
               country: str,
               poster: str,
               imdbRating: str,
               imdbId: str,
               type: str,
               totalSeasons: str,
               userId,
               table=table):
    db_config = read_db_config()
    cnx = MySQLConnection(**db_config)
    cursor = cnx.cursor(dictionary=True, buffered=True)

    q1 = (f"INSERT INTO {table} "
          "(title, year, released, genre, country, poster, imdbRating, imdbId, type, totalSeasons, userId)"
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    values = (title, year, released, genre, country,
              poster, imdbRating, imdbId, type, totalSeasons, userId)

    cursor.execute(q1, values)
    cnx.commit()
    cursor.close()
    cnx.close()
    row_id = cursor.lastrowid

    return ({"id": row_id, "message": "Success!", "valid": True}, 200)


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


def delete_serie_db(id, table=table):
    db_config = read_db_config()
    cnx = MySQLConnection(**db_config)
    cursor = cnx.cursor(dictionary=True, buffered=True)
    sql = f"DELETE FROM {table} WHERE id = '%s'" % (id)
    cursor.execute(sql)

    cnx.commit()
    cursor.close()
    cnx.close()

    return ({"message": "Success!", "valid": True}, 200)
