import os

import streamlit as st

from questions.Question import Question
from questions.SpectralQuestion import SpectralQuestion


class QuestionDrawer:
    """Public class for displaying questions"""

    @staticmethod
    def evaluateAnswer(current_question: Question, user_input: any, quiz=None, question_index: int = None) -> None:
        """Evaluates the answer after submitting it"""
        if (user_input is not None) or (user_input == 0):
            is_correct, feedback = current_question.verifyAndFeedback(user_input)
            
            # Record answer if quiz context is provided
            if quiz is not None and question_index is not None:
                quiz.recordAnswer(question_index, is_correct)
            
            if is_correct:
                st.success(f"Your answer is correct!  \n {feedback}")
            else:
                st.error(f"Your answer is incorrect!  \n {feedback}")
        
    
    @staticmethod
    def drawQuestion(current_question: Question, quiz=None, question_index: int = None) -> None:
        """Draws the parts of the question that are the same for all questions

        Args:
            current_question (Question): The question that is aimed to be displayed
            quiz: Optional quiz instance for tracking attempts
            question_index (int): Optional index of the question in the quiz
        """
        with st.container():
            st.title(current_question.title)
            current_question.drawImage()
            # Check if we have a spectral question: in that case create a download button with _drawDownload
            if isinstance(current_question, SpectralQuestion):
                QuestionDrawer._drawDownload(current_question)
            st.text(current_question.bodytext)

            with st.form("form" + current_question.title, enter_to_submit=False):
                user_input = current_question.drawYourself()
                if st.form_submit_button("Submit Answer", key="submit_button_form"):
                    if user_input is not None:
                        QuestionDrawer.evaluateAnswer(current_question, user_input, quiz, question_index)

            def _reset_callback() -> None:
                st.session_state[current_question.widget_key] = current_question.default

            st.button("Reset", on_click=_reset_callback)
            # st.rerun()
            
    @staticmethod
    @st.fragment  # This is a fragment so the app doesn't rerun when clicking the download button
    def _drawDownload(current_question: Question) -> None:
        """Draws the download button for spectral data.

        The check to see if this is a
        spectral question is done inside the drawQuestion function.
        The filename for this file is the final component of the pathname of the file to be downloaded

        Args:
            current_question (Question): question for which the spectral data is to be downloaded
        """
        with open(current_question.imgpath) as f:
            st.download_button(
                "Download Spectral Data", f, file_name=os.path.basename(current_question.imgpath), icon=":material/file_download:"
            )
