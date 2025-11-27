import sqlite3

questions = [
    ("Which theme is used for naming the hostels at IIT Guwahati?",
     "Mountain ranges", "Ancient Indian kingdoms", "Rivers and tributaries", "Indian freedom fighters",
     "Rivers and tributaries"),
    ("In the notation '1, 2, 3, …', what are the three dots (…) called?", 
     "Apostrophe", "Ellipsis", "Augmentation ", "Colon", 
     "Ellipsis"),
    ("'Ranjana Sonawane is now a 12-digit number', read a 2010 Times of India headline. She became the first recipient of this number. What are we talking about?",
     "National Population Register (NPR) ID", "UIDAI ID", "Permanent Account Number", "Smart Card National Identity Number (SCNIN)",
     "UIDAI ID"),
    ("Sachin Tendulkar completed his 100th hundred on 16th March 2012 by clipping off a single towards the square leg. Who was the bowler?",
     "Saeed Ajmal", "Mashrafe Mortaza", "Shakib Al Hasan", "Rubel Hossain",
     "Shakib Al Hasan"),
    ("'Gorkha cap gets ______ in its name,' read a headline in The Telegraph. Which famous Assamese music maestro completes the sentence?",
     "Zubeenda", "Rupamda", "Sankardev ", "Bhupenda", 
     "Bhupenda"),
    ("Zubeen Garg made his Bollywood playback debut with which song?", 
     "Dil Tu Hi Bata – Krrish 3", "Jaane Kya Chahe Mann – Pyaar Ke Side Effects", "Jeena Kya Tere Bina - Kya Love Story Hai", "Ya Ali – Gangster", 
     "Ya Ali – Gangster"),
    ("What is the only food that never spoils naturally?", 
     "Rice", "Honey", "Cheese ", "Wheat", 
     "Honey"),
    ("Who wrote the famous line: 'The pen is mightier than the sword'?", 
     "Shakespeare", "George Orwell", "Oscar Wilde", "Edward Bulwer-Lytton", 
     "Edward Bulwer-Lytton"),
    ("Which state assembly recently passed a strict anti-polygamy bill in 2025, criminalizing second marriages without legal dissolution of the first marriage?", 
     "West Bengal", "Assam", "Uttar Pradesh", "Kerala", 
     "Assam"),
    ("Which countries will jointly host the 2026 FIFA World Cup?", 
     "United States, Canada, and Mexico", "Spain, Portugal, and Morocco", "England, Scotland, and Wales", "Brazil, Argentina, and Chile", 
     "United States, Canada, and Mexico")
]

conn = sqlite3.connect("quizverse.db")
c = conn.cursor()

# Clear existing questions first (important)
c.execute("DELETE FROM questions")

for q in questions:
    c.execute(
        "INSERT INTO questions(question, option1, option2, option3, option4, answer) VALUES (?,?,?,?,?,?)",
        q,
    )

conn.commit()
conn.close()

print("Questions reset and added!")
