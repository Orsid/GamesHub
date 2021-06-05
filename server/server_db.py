import sqlite3
from sqlite3 import Error


def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(r"gameshub.db")
    except Error as e:
        print(e)

    return conn


def create_user(user_data):
    conn = create_connection()

    # check if the userName is already taken
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users WHERE userName=?", (user_data[2],))

    result = cur.fetchone()[0]
    if result != 0:
        print('userName Exists!')
        return -1  # Error creating the user

    """
    Create a new user into the users table
    :param conn:
    :param userData:
    :return: user id
    """
    sql = ''' INSERT INTO users(firstName, lastName, userName, password, email)
              VALUES(?,?,?,?,?) '''

    cur.execute(sql, user_data)
    conn.commit()
    conn.close()
    return cur.lastrowid


def validate_user(login_user_data):
    conn = create_connection()

    """
    Query user by userName
    :param conn: the Connection object
    :param userName:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users WHERE userName=? AND password=?", login_user_data)

    result = cur.fetchone()[0]

    conn.close()

    if result == 0:
        print('User Not Found!')
        return -1
    else:
        print('User Exists!')
        return 1
