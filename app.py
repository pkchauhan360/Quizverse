import streamlit as st
import sqlite3
import bcrypt
import random

# ---------- DB SETUP ----------
conn = sqlite3.connect("quizverse.db", check_same_thread=False)
c = conn.cursor()

def add_user(username, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    c.execute("INSERT INTO users(username, password) VALUES (?,?)", (username, hashed))
    conn.commit()

def login_user(username, password):
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    data = c.fetchone()
    if data and bcrypt.checkpw(password.encode(), data[0]):
        return True
    return False

def load_questions():
    c.execute("SELECT id, question, option1, option2, option3, option4, answer FROM questions")
    return c.fetchall()

def save_score(username, score):
    c.execute("INSERT INTO scores(username, score) VALUES (?,?)", (username, score))
    conn.commit()

def get_leaderboard():
    c.execute("""
        SELECT username, MAX(score) as best_score
        FROM scores
        GROUP BY username
        ORDER BY best_score DESC
        LIMIT 10
    """)
    return c.fetchall()

# ---------- STREAMLIT UI ----------
st.title("Quizverse 🧠")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

menu = st.sidebar.radio("Menu", ["Login", "Signup"])

# ---------- AUTH PAGES ----------
if not st.session_state.logged_in:
    if menu == "Signup":
        st.subheader("Create an Account ✨")
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")
        if st.button("Sign Up"):
            if new_user and new_pass:
                try:
                    add_user(new_user, new_pass)
                    st.success("Account created! Go to Login.")
                except Exception as e:
                    st.error("Username might already exist.")
            else:
                st.warning("Please enter both username and password.")

    if menu == "Login":
        st.subheader("Login 🔑")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid username or password")

# ---------- 👇 STEP 5: QUIZ SYSTEM GOES HERE ----------
if st.session_state.logged_in:
    st.sidebar.write(f"Logged in as: {st.session_state.username}")

    # 🚪 LOGOUT BUTTON
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

    page = st.sidebar.selectbox("Go to", ["Take Quiz", "Leaderboard"])

    # ----- QUIZ PAGE -----
    if page == "Take Quiz":
        st.header("Quiz Time 📚")
    
    # Shuffle only once and keep consistent
        if "quiz_questions" not in st.session_state:
            questions = load_questions()
            random.shuffle(questions)
            st.session_state.quiz_questions = questions
        else:
            questions = st.session_state.quiz_questions

        # Show all questions
        user_answers = {}
        for qid, q, o1, o2, o3, o4, ans in questions:
                        
            options = ["Select an answer", o1, o2, o3, o4]
            user_answers[qid] = st.radio(
                q,
                options,
                index=0,   # ensure nothing selected initially
            key=f"q_{qid}"
            )
            
        if st.button("Submit Quiz"):
            
            if "Select an answer" in user_answers.values():
                st.warning("Please answer all questions before submitting.")
            else:
                # scoring happens here
                score = 0
                for qid, q, o1, o2, o3, o4, ans in questions:
                    selected = user_answers.get(qid)
                    if selected != "Select an answer" and selected == ans:
                        score += 1
                        
                # Check if user already has a higher score
                c.execute("SELECT MAX(score) FROM scores WHERE username=?", (st.session_state.username,))
                existing = c.fetchone()[0]

                if existing is None or score > existing:
                    save_score(st.session_state.username, score)
                    st.success(f"Your New High Score: {score} 🎉")
                else:
                    st.info(f"Your Score: {score} (Best: {existing})")

                st.success(f"Your Score: {score} / {len(questions)} ✅")

    # ----- LEADERBOARD PAGE -----
    if page == "Leaderboard":
        st.header("Leaderboard 🏆")
        rows = get_leaderboard()
        if not rows:
            st.info("No scores yet. Be the first to take the quiz!")
        else:
            for i, (uname, best_score) in enumerate(rows, start=1):
                st.write(f"{i}. {uname} — {best_score} points")
