# 🎓 Online Quiz System

An interactive **Online Quiz System** built with **Python, Streamlit, and SQLite**. Users can register, take a multiple-choice quiz, see their scores, and view a leaderboard of top performers.

---

## **Features**

- ✅ User registration and login
- ✅ Take a quiz with random questions
- ✅ Automatic score calculation
- ✅ Store quiz results in SQLite database
- ✅ Leaderboard to display top scores
- ✅ Interactive web interface using **Streamlit**

---

## **Project Structure**

online_quiz/
│
├─ app.py # Streamlit main application
├─ database.py # Database connection and query functions
├─ requirements.txt # Required Python libraries
└─ data/ # Optional folder for sample questions

---

## **Technologies Used**

- **Python 3.x**
- **Streamlit** – for interactive frontend
- **SQLite** – lightweight SQL database for storing users, questions, and scores
- **Pandas** – for displaying leaderboard tables

---

## **Setup Instructions**

1. **Clone the repository**

````bash
git clone <repository_url>
cd online_quiz

2. **Install dependencies**
```bash
pip install streamlit pandas

3. **Run the app**
```bash
streamlit run app.py

4. **Open the quiz**
Open the URL shown in your terminal (usually http://localhost:8501) in a web browser.

---

**Usage**

Go to Register and create a new account.

Navigate to Login and log in with your credentials.

Take the quiz by selecting answers for each question.

Submit your answers to see your score.

Check Leaderboard to view top scores.

````
