import mysql.connector
from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config
from dotenv import load_dotenv
load_dotenv()


def get_from_db(table):

    db_config = read_db_config()
    cnx = MySQLConnection(**db_config)
    cursor = cnx.cursor(dictionary=True, buffered=True)

    cursor.execute(f"""SELECT * FROM {table} """)
    countAll = cursor.fetchall()

    cursor.execute(f"""SELECT * FROM {table}  LIMIT 100""")
    myresult = cursor.fetchall()

    count = len(countAll)

    return myresult, count


def check_duplicated(table, column, value):
    db_config = read_db_config()
    cnx = MySQLConnection(**db_config)
    cursor = cnx.cursor(dictionary=True, buffered=True)

    cursor.execute(
        f"SELECT * FROM {table} WHERE {column} = '%s'" % (value))

    myresult = cursor.fetchall()
    if myresult:
        return True


def delete_from_db(id, table):
    db_config = read_db_config()
    cnx = MySQLConnection(**db_config)
    cursor = cnx.cursor(dictionary=True, buffered=True)
    sql = f"DELETE FROM {table} WHERE public_id = '%s'" % (id)
    cursor.execute(sql)

    cnx.commit()
    cursor.close()
    cnx.close()
