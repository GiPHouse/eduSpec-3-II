import streamlit as st

from managers.QuestionManager import QuestionManager
from navigation import (
    aboutPage,
    getDefaultQuestion,
    homePage,
    initTheme,
    settingsPage,
    showNavigation,
)
from QuestionDrawer import QuestionDrawer

query_params = st.query_params
requested_question = query_params.get("question")
session_question = st.session_state.get("current_question")
current_question_name = (requested_question or session_question)

if current_question_name is None:
    current_page = query_params.get("page")
    if current_page == "settings":
        st.session_state["current_page"] = "settings"
        settingsPage()
    elif current_page == "about":
        st.session_state["current_page"] = "about"
        aboutPage()
    else:
        st.session_state["current_page"] = "home"
        homePage()
else:
    question = QuestionManager.loadQuestion(current_question_name)
    QuestionDrawer.drawQuestion(question)

st.session_state["current_question"] = current_question_name
if requested_question != current_question_name:
    st.query_params["question"] = current_question_name

showNavigation()
initTheme()

