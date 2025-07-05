#!/usr/bin/python3
import mysql.connector
import MySQLdb


def connect_to_prodev():
    """Establish and return a connection to the alx_prodev database using mysql.connector."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="!UGO2811!",
        database="alx_prodev"
    )


def stream_users_in_batches(batch_size):
    """Generator that yields users from the database in batches using MySQLdb."""
    conn = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="!UGO2811!",
        db="alx_prodev"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, age FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows

    cursor.close()
    conn.close()


def batch_processing(batch_size):
    """Processes batches and prints users over the age of 25."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            user_id, name, email, age = user
            if age > 25:
                print(f"ID: {user_id}, Name: {name}, Email: {email}, Age: {age}")
