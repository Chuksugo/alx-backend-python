def stream_users_in_batches(batch_size):
    """Generator that yields users from the database in batches."""
    import MySQLdb

    # Connect to MySQL database
    conn = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="!UGO2811!",    # 🔁 Update this
        db="alx_prodev"            # 🔁 Update if needed
    )
    cursor = conn.cursor()

    # Query with user id
    cursor.execute("SELECT id, name, email, age FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows

    # Clean up
    cursor.close()
    conn.close()


def batch_processing(batch_size):
    """Processes batches and prints users over the age of 25."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            user_id, name, email, age = user
            if age > 25:
                print(f"ID: {user_id}, Name: {name}, Email: {email}, Age: {age}")
