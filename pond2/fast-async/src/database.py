import sqlite3

conn = sqlite3.connect('todos.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    status INTEGER NOT NULL
)
''')

# Commit changes
conn.commit()

# Close connection
conn.close()

print("'todos' Table created!")