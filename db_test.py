import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def run_server(argument1, argument2):
    db_file = 'database.db'
    conn = create_connection(db_file)
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT login FROM credentials WHERE login = {}".format("'" + argument1 + "'"))
        login = cur.fetchall()
        if len(login) > 0:
            cur.execute("SELECT password FROM credentials WHERE login = {}".format("'" + argument1 + "'"))
            password = cur.fetchall()[0][0]
            if password == argument2:
                conn.close()
                return True
    conn.close()
    return False


if __name__ == "__main__":
    print(run_server('alla', '\xff\xf1G\xd2s\xbe\x19\xff\xbem\xc5|\xcb\xb4\xba\xf2\x88-\xed\x01'))
