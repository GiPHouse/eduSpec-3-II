import streamlit as st

from Question import Question
from MultipleChoiceQuestion import MultipleChoiceQuestion
from IntegerQuestion import IntegerQuestion

class QuestionDrawer():
    
    
    @staticmethod
    def drawQuestion(current_question:Question):

        if current_question is MultipleChoiceQuestion:
            pass
        if current_question is IntegerQuestion:
            pass
        
        with st.container():
            st.title(current_question.title)
            st.image(current_question.imgpath) #if imgpath is None it just does nothing?
            st.text(current_question.bodytext)

            #depending on question we have an input field or smth

            #if st.button: check answer
            st.button("Submit Answer")

            st.button("Reset")

