import sqlite3

conn = sqlite3.connect('magazine.db')
c = conn.cursor()

c.execute('''CREATE TABLE authors
             (id INTEGER PRIMARY KEY, name TEXT)''')

c.execute('''CREATE TABLE magazines
             (id INTEGER PRIMARY KEY, name TEXT, category TEXT)''')

c.execute('''CREATE TABLE articles
             (id INTEGER PRIMARY KEY, title TEXT, author_id INTEGER, magazine_id INTEGER,
             FOREIGN KEY (author_id) REFERENCES authors (id),
             FOREIGN KEY (magazine_id) REFERENCES magazines (id))''')

conn.commit()
conn.close()
