#!/usr/bin/python3
import MySQLdb


def stream_user_ages():
    """Generator that yields one user age at a time from the database."""
    conn = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="!UGO2811!",
        db="alx_prodev"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")

    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield float(row[0])

    cursor.close()
    conn.close()


def compute_average_age():
    """Computes and prints the average age using the generator."""
    total = 0
    count = 0

    for age in stream_user_ages():
        total += age
        count += 1

    average = total / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    compute_average_age()
