import os

import streamlit as st

from questions.Question import Question
from questions.SpectralQuestion import SpectralQuestion


class QuestionDrawer:
    """Public class for displaying questions."""

    @staticmethod
    def evaluateAnswer(current_question: Question, user_input: any) -> None:
        """Evaluate the answer after submitting it."""
        if (user_input is not None) or (user_input == 0):
            is_correct, feedback = current_question.verifyAndFeedback(user_input)
            if is_correct:
                st.success(f"Your answer is correct!  \n {feedback}")
            else:
                st.error(f"Your answer is incorrect!  \n {feedback}")

    @staticmethod
    def drawQuestion(current_question: Question) -> None:
        """Draws the parts of the question that are the same for all questions

        Args:
            current_question (Question): The question that is aimed to be displayed
        """
        with st.container():
            st.title(current_question.title)
            current_question.drawImage()
            # Check if we have a spectral question: in that case create a download button with _drawDownload
            st.text(current_question.bodytext)

            def _handle_reset_drawing_question() -> None:
                nonce_key = f"{current_question.widget_key}__jsme_nonce"
                last_seen_key = f"{current_question.widget_key}__last_seen"
                if nonce_key in st.session_state:
                    st.session_state[nonce_key] += 1
                if last_seen_key in st.session_state:
                    st.session_state[last_seen_key] = current_question.default

            def _reset_callback() -> None:
                st.session_state[current_question.widget_key] = current_question.default
                _handle_reset_drawing_question()

            with st.form(
                "form" + current_question.title,
                enter_to_submit=False,
            ):
                user_input = current_question.drawYourself()

                left_col, right_col = st.columns([2, 1])

                with left_col:
                    submit_clicked = st.form_submit_button(
                        "Submit Answer",
                        key=f"submit_button_form_{current_question.name}",
                        type="primary",
                        icon=":material/check:",
                        width="stretch",
                    )

                with right_col:
                    st.form_submit_button(
                        "Reset",
                        key=f"reset_button_form_{current_question.name}",
                        on_click=_reset_callback,
                        icon=":material/refresh:",
                        width="stretch",
                    )

            if submit_clicked and user_input is not None:
                QuestionDrawer.evaluateAnswer(current_question, user_input)

            # Check if we have a spectral question: in that case create a download button with _drawDownload
            if isinstance(current_question, SpectralQuestion):
                QuestionDrawer._drawDownload(current_question)

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
        with open(current_question.spectralpath, "rb") as f:
            st.download_button(
                "Download Spectral Data",
                f,
                file_name=os.path.basename(current_question.spectralpath),
                icon=":material/file_download:",
            )
