import sqlite3

conn = sqlite3.connect('survey.db')

c = conn.cursor()
c.execute("DROP TABLE users")
c.execute("DROP TABLE survey")
c.execute("DROP TABLE question")
c.execute("DROP TABLE answer")
c.execute("CREATE TABLE users (username TEXT PRIMARY KEY, encryptedpassword TEXT NOT NULL)")
c.execute("CREATE TABLE survey (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL)")
c.execute("CREATE TABLE question (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, question_id INTEGER NOT NULL, question TEXT, FOREIGN KEY(title) REFERENCES survey(title))")
c.execute("CREATE TABLE answer (answer_id INTEGER PRIMARY KEY AUTOINCREMENT, question_id INTEGER NOT NULL, answer TEXT, FOREIGN KEY(question_id) REFERENCES question(question_id))")

conn.commit()
conn.close()
