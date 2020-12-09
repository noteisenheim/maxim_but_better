import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            cur = conn.cursor()
            cur.execute("CREATE TABLE credentials (login TEXT PRIMARY KEY, password TEXT NOT NULL)")
            cur.execute("INSERT INTO credentials (login, password) VALUES('alla', '\\xff\\xf1G\\xd2s\\xbe\\x19\\xff\\xbem\\xc5|\\xcb\\xb4\\xba\\xf2\\x88-\\xed\\x01'), ('amina', '\\xc2>w\\xc8\\x1a\\x15\\xdb\\x03\\x1a\\xef\\xdc\\xa8|\\xe2h3@\\xa2\\xa5\\xde')")
            conn.commit()
            conn.close()

if __name__ == '__main__':
    create_connection("database.db")
