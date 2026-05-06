from pathlib import Path

import streamlit as st

from managers.QuestionManager import QuestionManager
from managers.QuizManager import QuizManager
from navigation import initTheme, resolveQuestion, showNavigation
from QuestionDrawer import QuestionDrawer

quiz_dir = Path(__file__).resolve().parent.parent / "data" / "quizzes"


def getAvailableQuizzes() -> list[str]:
    """Return all quiz ids available in the data/quizzes directory."""
    if not quiz_dir.exists():
        return []
    return sorted(path.stem for path in quiz_dir.glob("*.json"))


initTheme()

available_quizzes = getAvailableQuizzes()
quiz_options = [""] + available_quizzes
current_quiz = st.session_state.get("current_quiz") or ""

st.sidebar.divider()
selected_quiz = st.sidebar.selectbox(
    "Quiz",
    options=quiz_options,
    index=quiz_options.index(current_quiz) if current_quiz in quiz_options else 0,
    format_func=lambda quiz_name: "Browse questions" if quiz_name == "" else quiz_name,
    key="quiz_selector",
)

if selected_quiz:
    st.session_state["current_quiz"] = selected_quiz
    quiz = QuizManager.loadQuiz(selected_quiz)
    quiz.drawQuiz()
else:
    st.session_state["current_quiz"] = None
    query_params = st.query_params
    requested_question = query_params.get("question")
    session_question = st.session_state.get("current_question")
    current_question_name = resolveQuestion(requested_question or session_question)

    st.session_state["current_question"] = current_question_name
    if requested_question != current_question_name:
        st.query_params["question"] = current_question_name

    showNavigation()

    question = QuestionManager.loadQuestion(current_question_name)
    QuestionDrawer.drawQuestion(question)