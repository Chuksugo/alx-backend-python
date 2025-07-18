#!/usr/bin/env python3
import asyncio
import aiosqlite

DB_PATH = "my_database.db"  # Update path if necessary


async def async_fetch_users():
    """Fetch all users from the database."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows  


async def async_fetch_older_users():
    """Fetch users older than 40 from the database."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            return rows  


async def fetch_concurrently():
    """Fetch users concurrently using asyncio.gather."""
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("All users:")
    for user in all_users:
        print(user)

    print("\nUsers older than 40:")
    for user in older_users:
        print(user)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
