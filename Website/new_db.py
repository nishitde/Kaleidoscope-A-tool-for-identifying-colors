import sqlite3

conn = sqlite3.connect('kaleidoscope.db')

c = conn.cursor()
c.execute("DROP TABLE Images")
c.execute("DROP TABLE colors")
c.execute("CREATE TABLE Images (Name TEXT NOT NULL UNIQUE)")
c.execute("CREATE TABLE colors (Name TEXT NOT NULL)")

conn.commit()
conn.close()
