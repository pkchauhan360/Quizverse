import sqlite3
from datetime import datetime
import random

DB_NAME = "quiz.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS Users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                )''')
    
    # Questions table
    c.execute('''CREATE TABLE IF NOT EXISTS Questions (
                    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT,
                    correct_option TEXT
                )''')
    
    # Options table
    c.execute('''CREATE TABLE IF NOT EXISTS Options (
                    option_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id INTEGER,
                    option_label TEXT,
                    option_text TEXT,
                    FOREIGN KEY(question_id) REFERENCES Questions(question_id)
                )''')
    
    # Scores table
    c.execute('''CREATE TABLE IF NOT EXISTS Scores (
                    score_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    score INTEGER,
                    date_taken TEXT,
                    FOREIGN KEY(user_id) REFERENCES Users(user_id)
                )''')
    
    conn.commit()
    conn.close()

def add_sample_data():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Check if sample questions exist
    c.execute("SELECT COUNT(*) FROM Questions")
    if c.fetchone()[0] > 0:
        conn.close()
        return
    
    # Sample questions
    questions = [
        ("What is the capital of France?", "B"),
        ("Which language is used for data science?", "C")
    ]
    options = [
        [("A","Berlin"),("B","Paris"),("C","Rome"),("D","Madrid")],
        [("A","Java"),("B","C++"),("C","Python"),("D","HTML")]
    ]
    
    for i, (q_text, correct) in enumerate(questions):
        c.execute("INSERT INTO Questions (question, correct_option) VALUES (?,?)", (q_text, correct))
        q_id = c.lastrowid
        for label, text in options[i]:
            c.execute("INSERT INTO Options (question_id, option_label, option_text) VALUES (?,?,?)",
                      (q_id, label, text))
    
    conn.commit()
    conn.close()

def get_random_questions(n=5):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f"SELECT question_id, question, correct_option FROM Questions ORDER BY RANDOM() LIMIT {n}")
    questions = c.fetchall()
    result = []
    for q_id, question, correct in questions:
        c.execute("SELECT option_label, option_text FROM Options WHERE question_id=?", (q_id,))
        opts = c.fetchall()
        random.shuffle(opts)  # Shuffle options
        result.append({"id": q_id, "question": question, "correct": correct, "options": opts})
    conn.close()
    return result

def register_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO Users (username, password) VALUES (?,?)", (username, password))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT user_id FROM Users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user[0] if user else None

def save_score(user_id, score):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO Scores (user_id, score, date_taken) VALUES (?,?,?)", 
              (user_id, score, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_leaderboard():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT u.username, MAX(s.score) as high_score 
        FROM Scores s 
        JOIN Users u ON s.user_id = u.user_id 
        GROUP BY u.username 
        ORDER BY high_score DESC
    """)
    leaderboard = c.fetchall()
    conn.close()
    return leaderboard
