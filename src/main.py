import streamlit as st

from managers.QuestionManager import QuestionManager
from managers.QuizManager import QuizManager
from navigation import (
    aboutPage,
    getTopLevelQuestionLabel,
    getTopLevelQuizLabel,
    homePage,
    initTheme,
    settingsPage,
    showNavigation,
)
from QuestionDrawer import QuestionDrawer

initTheme()

query_params = st.query_params
requested_quiz = query_params.get("quiz")
requested_question = query_params.get("question")
session_quiz = st.session_state.get("current_quiz")
session_question = st.session_state.get("current_question")

current_quiz_name = requested_quiz or (None if requested_question else session_quiz)
current_question_name = None if current_quiz_name else requested_question or session_question

if current_quiz_name:
    st.session_state["current_quiz"] = current_quiz_name
    st.session_state["current_question"] = None
    st.session_state["current_page"] = None
    st.session_state["navbar"] = getTopLevelQuizLabel(current_quiz_name)
    st.query_params["quiz"] = current_quiz_name
    st.query_params.pop("question", None)
    st.query_params.pop("page", None)
    showNavigation()
    quiz = QuizManager.loadQuiz(current_quiz_name)
    quiz.drawQuiz()
elif current_question_name:
    st.session_state["current_quiz"] = None
    st.session_state["current_question"] = current_question_name
    st.session_state["navbar"] = getTopLevelQuestionLabel(current_question_name)
    if requested_question != current_question_name:
        st.query_params["question"] = current_question_name
    st.query_params.pop("quiz", None)
    showNavigation()
    question = QuestionManager.loadQuestion(current_question_name)
    QuestionDrawer.drawQuestion(question)
else:
    current_page = query_params.get("page")
    if current_page and current_page.lower() == "settings":
        st.session_state["current_page"] = "settings"
        settingsPage()
    elif current_page and current_page.lower() == "about":
        st.session_state["current_page"] = "about"
        aboutPage()
    else:
        st.session_state["current_page"] = "home"
        homePage()
    showNavigation()
    

