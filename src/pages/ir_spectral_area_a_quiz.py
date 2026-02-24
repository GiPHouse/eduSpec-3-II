import streamlit as st

from components.navigation import showIrSidebar, showNavbar
from QuizBuilder import QuizBuilder

showNavbar()
st.title("Mini Quiz \n Area A (3800 - 3200 cm-1)")
st.write("Welcome to the IR Spectral Areas A Page!")
showIrSidebar()


quiz = QuizBuilder.buildQuiz("this is a quiz", ["selam"])
quiz.drawQuiz()
