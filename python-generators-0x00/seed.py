import mysql.connector
import csv
import uuid


def connect_db():
    """Connect to MySQL server (no specific DB yet)"""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="!UGO2811!"  # replace with your MySQL password
    )

def create_database(connection):
    """Create ALX_prodev DB if it doesn't exist"""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    cursor.close()

def connect_to_prodev():
    """Connect to the ALX_prodev database"""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="!UGO2811!",  # replace with your MySQL password
        database="ALX_prodev"
    )

def create_table(connection):
    """Create user_data table if it doesn't exist"""
    cursor = connection.cursor()
    create_query = '''
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(5, 2) NOT NULL
    );
    '''
    cursor.execute(create_query)
    connection.commit()
    print("Table user_data created successfully")
    cursor.close()

def insert_data(connection, filename):
    """Insert data from CSV into the user_data table"""
    cursor = connection.cursor()
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        print("CSV Headers:", reader.fieldnames)  # Optional: debug check
        for row in reader:
            try:
                user_id = str(uuid.uuid4())  # Generate a unique ID
                cursor.execute('''
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                ''', (user_id, row['name'], row['email'], row['age']))
            except Exception as e:
                print(f"Insertion error: {e}")
    connection.commit()
    cursor.close()

