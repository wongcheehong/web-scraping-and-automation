import sqlite3

conn = sqlite3.connect('undercover.db')

c = conn.cursor()

c.execute("""CREATE TABLE OnlineWordPairs (
            id integer primary key autoincrement,
            word1 text collate nocase,
            word2 text collate nocase,
            hasBeenPlayed integer
        )""")

conn.commit()

conn.close()
