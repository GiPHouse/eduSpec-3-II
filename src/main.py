"""The application itself"""

import streamlit as st

from Question import Question

st.write("""
Hello world
""")

# mcq = MultipleChoiceQuestion("title","hi",["aaa","bbb"],0,["true","false"])
# QuestionDrawer.drawQuestion(mcq)

x = Question("a", "b")
