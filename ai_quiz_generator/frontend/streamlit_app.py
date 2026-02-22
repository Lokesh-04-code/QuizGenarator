import streamlit as st
import requests

st.set_page_config(page_title="AI Quiz Generator", layout="wide")
st.title("🧠 AI Quiz Generator")

BACKEND_URL = "http://localhost:8000"

if "quiz" not in st.session_state:
    st.session_state.quiz = None

# Upload
files = st.file_uploader("Upload Documents", accept_multiple_files=True)

if st.button("Process Documents"):
    if files:
        payload = [("files", (f.name, f, f.type)) for f in files]
        requests.post(f"{BACKEND_URL}/upload", files=payload)
        st.success("Documents Processed")

# Config
model = st.selectbox("Model", [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "moonshotai/kimi-k2-instruct-0905"
])

single_n = st.number_input("Single MCQ", 0, 10, 2)
multi_n = st.number_input("Multi MCQ", 0, 10, 2)
tf_n = st.number_input("True/False", 0, 10, 2)
yn_n = st.number_input("Yes/No", 0, 10, 2)

if st.button("Generate Quiz"):

    response = requests.post(
        f"{BACKEND_URL}/generate",
        data={
            "single_n": single_n,
            "multi_n": multi_n,
            "tf_n": tf_n,
            "yn_n": yn_n,
            "model": model
        }
    )

    if response.status_code == 200:
        data = response.json()
        if "error" in data:
            st.error(data["error"])
        else:
            st.session_state.quiz = data
    else:
        st.error("Backend error occurred")


# ================= DISPLAY =================
if st.session_state.quiz:

    questions = st.session_state.quiz["questions"]

    for i, q in enumerate(questions):

        st.markdown("---")
        st.markdown(f"### Question {i+1}")
        st.write(q["text"])

        # SINGLE
        if q["type"] == "single":
            correct_index = q["options"].index(q["correctAnswer"])

            st.radio(
                "Select one:",
                q["options"],
                index=correct_index,
                key=q["id"]
            )

            st.success(f"Correct Answer: {q['correctAnswer']}")
            st.info(f"Explanation: {q['explanation']}")

        # MULTI (AUTO-MAP CORRECT OPTIONS)
        elif q["type"] == "multi":

            st.write("Select one or more options:")

            correct_set = set(q["correctAnswer"])

            for opt in q["options"]:
                st.checkbox(
                    opt,
                    value=(opt in correct_set),   # auto-check correct ones
                    key=f"{q['id']}_{opt}"
                )

            st.success(f"Correct Answers: {', '.join(q['correctAnswer'])}")
            st.info(f"Explanation: {q['explanation']}")

        # TRUE/FALSE
        elif q["type"] == "truefalse":
            correct_index = q["options"].index(q["correctAnswer"])

            st.radio(
                "Select:",
                q["options"],
                index=correct_index,
                key=q["id"]
            )

            st.success(f"Correct Answer: {q['correctAnswer']}")
            st.info(f"Explanation: {q['explanation']}")

        # YES/NO
        elif q["type"] == "yesno":
            correct_index = q["options"].index(q["correctAnswer"])

            st.radio(
                "Select:",
                q["options"],
                index=correct_index,
                key=q["id"]
            )

            st.success(f"Correct Answer: {q['correctAnswer']}")
            st.info(f"Explanation: {q['explanation']}")

    st.markdown("---")
    st.markdown("### JSON Output")
    st.json(st.session_state.quiz)