import sqlite3

# DB file
DATABASE_FILE = "chat_history.db"

def create_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # create table to store chat messages
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                      id INTEGER PRIMARY KEY,
                      message TEXT NOT NULL,
                      timestamp TEXT NOT NULL
                      )''')

    conn.commit()
    conn.close()

# create DB
create_database()

print("Database 'chat_history.db' has been created successfully.")
