#!/usr/bin/env python3
import sqlite3

class ExecuteQuery:
    def __init__(self, db_file, query, params=None):
        self.db_file = db_file
        self.query = query
        self.params = params if params else []
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    db_path = "my_database.db"  # Replace with your actual database file

    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery(db_path, query, params) as results:
        for row in results:
            print(row)
