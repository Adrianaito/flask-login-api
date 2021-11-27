from dbconfig import read_db_config
from mysql.connector import MySQLConnection, Error
from Modules.DB.UsersDb import create_user


def connect():
    """ Connect to MySQL database """

    db_config = read_db_config()
    conn = None
    try:
        print("Connecting to MySQL database...")
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print("Connection established.")

            cursor = conn.cursor()
            cursor.execute("SELECT VERSION()")

            row = cursor.fetchone()
            print("Server version:", row[0])

            role = 0
            email = "test@gmail.com"
            password = "test"
            create_user(email, password)

            # cursor.execute("DESCRIBE comments")
            # for x in cursor:
            #     print(x)

        else:
            print("Connection failed.")

    except Exception as error:
        print(error)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
            print("Connection closed.")


if __name__ == "__main__":
    connect()
