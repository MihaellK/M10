import sqlite3


# Database creation
def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("'users' table created!")

create_database()  # Call the function to create the database if it doesn't exist

# Database connection
def db_connect():
    return sqlite3.connect('users.db')
