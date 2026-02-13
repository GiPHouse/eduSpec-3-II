from Question import Question
from MultipleChoiceQuestion import MultipleChoiceQuestion
import streamlit as st

class QuestionDrawer():
    
    @staticmethod
    def drawQuestion(current_question:Question):

        if isinstance(current_question, MultipleChoiceQuestion):
            pass

    @staticmethod    
    def drawMCP(mcp:MultipleChoiceQuestion, qid: str):

        chosen_key = qid + "_chosen"        # selected option by the user
        submitted_key = qid + "_submitted"  # boolean to check if the user has submitted an answer
        result_key = qid + "_result"        # tuple of (is_correct: bool, feedback: str)

        with st.container():
            # Display the question title and body text
            if getattr(mcp, "title", None):
                st.markdown(f"### {mcp.title}")
            if getattr(mcp, "bodytext", None):
                st.markdown(mcp.bodytext)

            # Image display if imgpath is provided    
            imgpath = getattr(mcp, "imgpath", None)
            if imgpath:
                st.image(imgpath, width="stretch")

            # Options (Radio in streamlit)
            selected_option = st.radio("Pick one", mcp.answers, key=chosen_key)

            # Submit button (TBD)

            # Feedback after submission (TBD)