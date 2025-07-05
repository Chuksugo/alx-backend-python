import mysql.connector

def stream_users():
    """Generator that yields rows from user_data table one by one"""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="!UGO2811!",  # use your correct password
        database="ALX_prodev"
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()
