import streamlit as st

from IntegerQuestion import IntegerQuestion
from MultipleChoiceQuestion import MultipleChoiceQuestion
from QuestionDrawer import QuestionDrawer
from WordQuestion import WordQuestion

st.switch_page("pages/home.py")

questionint = IntegerQuestion(
    "title",
    "this is the body text",
    (10, 20),
    ["correct", "wrong too small", "wrong too big"],
    imgpath="../data/test.png",
)


questionmult = MultipleChoiceQuestion(
    "title",
    "this is the body text",
    ["10", "20", "30", "40"],
    2,
    ["a", "b", "c", "d"],
    imgpath="../data/test.png",
)

questionstr = WordQuestion(
    "title",
    "this is the body text",
    "answer",
    ["correct", "wrong"],
    imgpath="../data/test.png",
)

QuestionDrawer.drawQuestion(questionstr)


# QuestionDrawer.drawQuestion(questionmult)
