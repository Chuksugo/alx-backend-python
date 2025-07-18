#!/usr/bin/env python3
import sqlite3

class DatabaseConnection:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.cursor = None

    def __enter__(self):
        # Open connection and return the cursor
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Commit changes (if any), close cursor and connection
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    db_path = "my_database.db"  # Replace with your actual database path

    with DatabaseConnection(db_path) as cursor:
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
