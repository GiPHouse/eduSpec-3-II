import streamlit as st

from MultipleChoiceQuestion import MultipleChoiceQuestion
from QuestionDrawer import QuestionDrawer

st.write("""
Hello world
""")

mcq = MultipleChoiceQuestion("title", "hi", ["aaa", "bbb"], 0, ["true", "false"])
QuestionDrawer.drawQuestion(mcq)
