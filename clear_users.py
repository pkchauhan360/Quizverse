import sqlite3

# connect to your database file
conn = sqlite3.connect("quizverse.db")
c = conn.cursor()

# delete all users
c.execute("DELETE FROM users")

# delete all scores
c.execute("DELETE FROM scores")

conn.commit()
conn.close()

print("All users and their scores have been deleted.")
