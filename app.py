import streamlit as st
from database import create_tables, add_sample_data, register_user, login_user, get_random_questions, save_score, get_leaderboard

# Initialize DB and sample data
create_tables()
add_sample_data()

st.title("🎓 Online Quiz System")

# Sidebar navigation
menu = ["Login", "Register", "Leaderboard"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":
    st.subheader("Create a new account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if register_user(username, password):
            st.success("Account created! You can now login.")
        else:
            st.error("Username already exists.")

elif choice == "Login":
    st.subheader("Login to take quiz")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user_id = login_user(username, password)
        if user_id:
            st.success(f"Welcome {username}! Let's start the quiz.")
            
            # Load quiz
            questions = get_random_questions(5)
            answers = {}
            
            for i, q in enumerate(questions):
                st.write(f"**Q{i+1}: {q['question']}**")
                options = [f"{label}: {text}" for label, text in q['options']]
                ans = st.radio("Choose an option", options, key=i)
                answers[q['id']] = ans[0]  # get label (A/B/C/D)
            
            if st.button("Submit Answers"):
                score = 0
                for q in questions:
                    if answers[q['id']] == q['correct']:
                        score += 1
                save_score(user_id, score)
                st.success(f"You scored {score} / {len(questions)}")
        else:
            st.error("Invalid credentials.")

elif choice == "Leaderboard":
    st.subheader("🏆 Leaderboard")
    leaderboard = get_leaderboard()
    st.table(leaderboard)
