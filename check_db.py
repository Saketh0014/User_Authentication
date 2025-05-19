import sqlite3

DB_PATH = 'LoginData.db'

def check_db():
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in database:", tables)
        if ('USERS',) in tables:
            cursor.execute("PRAGMA table_info(USERS);")
            columns = cursor.fetchall()
            print("USERS table columns:", columns)
        else:
            print("USERS table does not exist.")
        connection.close()
    except Exception as e:
        print("Error accessing database:", e)

if __name__ == '__main__':
    check_db()
