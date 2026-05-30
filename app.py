import streamlit as st
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("key")
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    openai_api_key=os.getenv("key")
)
st.title("📘 AI Quiz App")

# ---------- SESSION STATE ----------

if "questions" not in st.session_state:
    st.session_state.questions = []

if "correct" not in st.session_state:
    st.session_state.correct = []

if "user" not in st.session_state:
    st.session_state.user = []

if "index" not in st.session_state:
    st.session_state.index = 0

if "started" not in st.session_state:
    st.session_state.started = False


# ---------- QUIZ SETUP ----------

if not st.session_state.started:

    topic = st.text_input("Enter Topic")
    difficulty = st.selectbox("Select Difficulty", ["easy","medium","hard"])
    t=st.number_input("Number of Questions",min_value=1, max_value=20, value=1)
    if difficulty == "easy":
        total = t
    elif difficulty == "medium":
        total = t
    else:
        total = t

    if st.button("Generate Quiz"):

        prompt = f"""
        Generate {total} MCQ questions on topic: {topic}
        Difficulty: {difficulty}

        FORMAT:

        Q: question?
        A) option
        B) option
        C) option
        D) option
        CORRECT: A
        ---
        """

        res = llm.invoke(prompt).content

        blocks = res.split("---")

        for b in blocks:
            if "CORRECT:" in b:
                q, a = b.split("CORRECT:")
                st.session_state.questions.append(q.strip())
                st.session_state.correct.append(a.strip())

        st.session_state.started = True
        st.rerun()


# ---------- QUIZ START ----------

if st.session_state.started:

    i = st.session_state.index

    # If quiz not finished
    if i < len(st.session_state.questions):

        st.subheader(f"Question {i+1}")

        st.write(st.session_state.questions[i])

        ans = st.radio(
            "Your Answer",
            ["A","B","C","D"],
            key=i
        )

        if st.button("Next"):

            st.session_state.user.append(ans)
            st.session_state.index += 1
            st.rerun()

    # ---------- RESULT ----------
    else:
        score = 0
        wrong = []

        for i in range(len(st.session_state.correct)):
            if st.session_state.user[i] == st.session_state.correct[i]:
                score += 1
            else:
                wrong.append(i)

        st.success(f"Your Score: {score} / {len(st.session_state.correct)}")

        
        if len(wrong) == 0:
            st.balloons()
            st.write("🎉 All answers correct!")
        else:
            st.subheader("Wrong Answers Review")

            for i in wrong:
                st.write("----")
                st.write(st.session_state.questions[i])
                st.write("Your Answer:", st.session_state.user[i])
                st.write("Correct Answer:", st.session_state.correct[i])

        if st.button("Restart"):
            st.session_state.clear()
            st.rerun()
