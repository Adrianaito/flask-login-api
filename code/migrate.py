from dbconfig import read_db_config
from mysql.connector import MySQLConnection, Error


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

            # ********************************************************************************************

            # CAUTION: UNCOMMENTING THE FOLLOWING LINES AND RUNNING THE CODE WILL DROP TABLES PERMANENTLY!

            # ********************************************************************************************

            # cursor.execute("DROP TABLE IF EXISTS users")
            # sql = '''CREATE TABLE users(
            # id INT NOT NULL PRIMARY KEY AUTO_INCREMENT UNIQUE,
            # public_id VARCHAR(45) NOT NULL UNIQUE,
            # name CHAR(20),
            # email CHAR(45) NOT NULL UNIQUE,
            # password VARCHAR(1000) NOT NULL,
            # role INT NOT NULL
            # )'''
            # cursor.execute(sql)
            # print("created table responses")

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
