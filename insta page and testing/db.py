import mysql.connector

def get_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="102030",
        database="instagram_clone",
        auth_plugin='mysql_native_password'
    )
    cursor = conn.cursor(dictionary=True)
    return conn, cursor
