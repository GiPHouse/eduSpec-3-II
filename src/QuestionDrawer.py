from Question import Question
from MultipleChoiceQuestion import MultipleChoiceQuestion
import streamlit as st

class QuestionDrawer():
    
    @staticmethod
    def drawQuestion(current_question:Question):

        if isinstance(current_question, MultipleChoiceQuestion):
            pass

    @staticmethod    
    def drawMCQ(mcq:MultipleChoiceQuestion, qid: str):

        chosen_key = qid + "_chosen"        # selected option by the user
        submitted_key = qid + "_submitted"  # boolean to check if the user has submitted an answer
        result_key = qid + "_result"        # tuple of (is_correct: bool, feedback: str)

        with st.container():
            # Display the question title and body text
            if getattr(mcq, "title", None):
                st.markdown(f"### {mcq.title}")
            if getattr(mcq, "bodytext", None):
                st.markdown(mcq.bodytext)

            # Image display if imgpath is provided    
            imgpath = getattr(mcq, "imgpath", None)
            if imgpath:
                st.image(imgpath, width="stretch")

            # Options (Radio in streamlit)
            selected_option = st.radio("Pick one", mcq.answers, key=chosen_key)

            # Submit button (TBD)
            '''# 4) Submit Answer button (only button inside drawer)
            if st.button("Submit Answer", key=f"{qid}_submit"):
                selected_index = mcq.answers.index(selected_option)
                is_correct, feedback = mcq.verifyAndFeedback(selected_index)

                st.session_state[submitted_key] = True
                st.session_state[result_key] = (is_correct, feedback)'''


            # Feedback after submission (TBD)