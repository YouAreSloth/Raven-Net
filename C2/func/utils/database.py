import sqlite3
import base64
import os

class DBController:
    def __init__(self, db_path='./user.db'):
        self.db_path = db_path
        self._create_db_if_not_exists()
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT,
                                password TEXT,
                                rank INT)''')
        self.conn.commit()

    def _create_db_if_not_exists(self):
        if not os.path.exists(self.db_path):
            open(self.db_path, 'w').close()
            print(f"Database created: {self.db_path}")  # Debug print

    def get_username_by_id(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        return self.cursor.fetchone()

    def get_id_by_username(self, username):
        self.cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        result = self.cursor.fetchone()
        return result

    def get_rank_by_username(self, username):
        self.cursor.execute('SELECT rank FROM users WHERE username = ?', (username,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def change_password(self, user_id, new_password):
        encoded_password = base64.b64encode(new_password.encode()).decode()
        self.cursor.execute('UPDATE users SET password = ? WHERE id = ?', (encoded_password, user_id))
        self.conn.commit()

    def add_user(self, username, password, rank):
        encoded_password = base64.b64encode(password.encode()).decode()
        self.cursor.execute('INSERT INTO users (username, password, rank) VALUES (?, ?, ?)',
                            (username, encoded_password, rank))
        self.conn.commit()

    def close(self):
        self.conn.close()