import sqlite3

DB_PATH = 'LoginData.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_all_users():
    connection = get_connection()
    cursor = connection.cursor()
    users = cursor.execute("SELECT first_name, last_name, email FROM USERS").fetchall()
    connection.close()
    return [{'first_name': u[0], 'last_name': u[1], 'email': u[2]} for u in users]

def get_user_by_email(email):
    connection = get_connection()
    cursor = connection.cursor()
    user = cursor.execute("SELECT first_name, last_name, email, password FROM USERS WHERE email = ?", (email,)).fetchone()
    connection.close()
    if user:
        return {'first_name': user[0], 'last_name': user[1], 'email': user[2], 'password': user[3]}
    return None

def get_user_by_email_and_username(email, username):
    connection = get_connection()
    cursor = connection.cursor()
    user = cursor.execute("SELECT first_name, last_name, email, password FROM USERS WHERE email = ? AND first_name = ?", (email, username)).fetchone()
    connection.close()
    if user:
        return {'first_name': user[0], 'last_name': user[1], 'email': user[2], 'password': user[3]}
    return None

def create_user(first_name, last_name, email, password):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO USERS (first_name, last_name, email, password) VALUES (?, ?, ?, ?)",
                   (first_name, last_name, email, password))
    connection.commit()
    connection.close()

def clear_all_data():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM USERS")
    connection.commit()
    connection.close()

def get_user_by_username_and_password(username, password):
    connection = get_connection()
    cursor = connection.cursor()
    user = cursor.execute("SELECT first_name, last_name, email FROM USERS WHERE first_name = ? AND password = ?", (username, password)).fetchone()
    connection.close()
    if user:
        return {'first_name': user[0], 'last_name': user[1], 'email': user[2]}
    return None
