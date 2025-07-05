# Python Generators - Task 0: Getting Started with Python Generators

## 🧠 Objective

Create a generator system that connects to a MySQL database and streams rows one-by-one using Python. This task focuses on database setup, data insertion, and preparing for generator-based streaming.

---

## 📦 Requirements

- Python 3
- MySQL Server
- `mysql-connector-python` package
- A CSV file named `user_data.csv` containing sample user records

---

## 📁 Files

- `0-main.py`: Main script to test and verify the database connection and table setup.
- `seed.py`: Contains functions to connect to MySQL, create the database, create tables, and insert data.
- `user_data.csv`: Sample user data used to populate the database.
- `README.md`: Documentation file (this one).

---

## 🚀 Setup Instructions

1. Install MySQL and start the MySQL server.
2. Install the MySQL connector:
   ```bash
   pip install mysql-connector-python
