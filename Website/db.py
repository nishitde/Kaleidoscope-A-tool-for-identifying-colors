import os
import re
import sqlite3

SQLITE_PATH = os.path.join(os.path.dirname(__file__), 'survey.db')

class Database:

    def __init__(self):
        self.conn = sqlite3.connect(SQLITE_PATH)

    def select(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        return c.fetchall()

    def execute(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        self.conn.commit()

    def create_user(self, username, encryptedpassword):
        self.execute('INSERT OR IGNORE INTO users (username, encryptedpassword) VALUES (?, ?)', [username, encryptedpassword])

    def get_user(self, username):
        data = self.select('SELECT * FROM users WHERE username=?', [username])
        if data:
            d = data[0]
            return {
                'username': d[0],
                'encryptedpassword': d[1],
            }
        else:
            return None

    def create_survey(self, title):
        self.execute('INSERT OR IGNORE INTO survey (title) VALUES (?)', [title])

    def create_question(self, title, question_id, question):
        self.execute('INSERT OR IGNORE INTO question (title, question_id, question) VALUES (?, ?, ?)', [title, question_id, question])

    def create_answer(self, question_id, answer):
        self.execute('INSERT OR IGNORE INTO answer (question_id, answer) VALUES (?, ?)', [question_id, answer])

    def close(self):
        self.conn.close()
