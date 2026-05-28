from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("key")
# ---------- LOAD VECTOR DB ----------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    "my_db",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = db.as_retriever()

# ---------- LLM (OPENROUTER FIX) ----------
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    openai_api_key=os.getenv("key")
)


# ---------- USER INPUT ----------
print("----- QUIZ SETUP -----")

topic = input("Enter topic: ")
difficulty = input("Difficulty (easy/medium/hard): ")
t=int(input("Number of questions: "))
if difficulty == "easy":
    total = t
elif difficulty == "medium":
    total = t
else:
    total = t


prompt = f"""
Generate {total} MCQ questions on topic: {topic}
Difficulty: {difficulty}

STRICT FORMAT:

Q: question?
A) option
B) option
C) option
D) option
CORRECT: A
---
"""

response = llm.invoke(prompt)

quiz = response.content.strip()

blocks = quiz.split("---")

questions = []
correct_answers = []

for b in blocks:
    if "CORRECT:" in b:
        q, a = b.split("CORRECT:")
        questions.append(q.strip())
        correct_answers.append(a.strip())

# -------- QUIZ START --------

user_answers = []

print("\n===== START QUIZ =====")

for i in range(len(questions)):
    print(f"\nQuestion {i+1}")
    print(questions[i])

    ans = input("Your Answer (A/B/C/D): ").strip().upper()
    user_answers.append(ans)

# -------- RESULT --------

score = 0

for i in range(len(correct_answers)):
    if user_answers[i] == correct_answers[i]:
        score += 1
score = 0
wrong_index = []

for i in range(len(correct_answers)):
    if user_answers[i] == correct_answers[i]:
        score += 1
    else:
        wrong_index.append(i)
if len(wrong_index) == 0:
    print("\n🎉 Excellent! All answers are correct.")
else:
    print("\n===== WRONG ANSWERS REVIEW =====")

    for i in wrong_index:
        print(f"\nQuestion {i+1}")
        print(questions[i])
        print("Your Answer   :", user_answers[i])
        print("Correct Answer:", correct_answers[i])


print("\n===== FINAL RESULT =====")
print(f"Your Score: {score} / {len(correct_answers)}")