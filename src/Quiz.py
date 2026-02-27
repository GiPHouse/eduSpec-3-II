import streamlit as st

from Question import Question
from QuestionDrawer import QuestionDrawer


class Quiz:
    """Class to create the elements of a quiz.

    It picks the right question for the page and makes previous and next button depending on the questions
    """

    def __init__(self, name: str, question_list: list[Question]) -> None:
        """Initialises a quiz instance.

        Args:
            name (str): The unique name/id of the quiz.
            question_list (list[Question]): A list of questions in the quiz.
        """
        if "current_index" not in st.session_state:
            st.session_state["current_index"] = 0
        self.current_index = 0
        self.question_list = question_list
        self.name = name

    def drawPreviousButton(self) -> None:
        """Draws a button to go to the previous question.

        The check whether there is a previous question is done in drawNextButton
        """

        def _previous_callback() -> None:
            """Changes the session_state to the session_state of the previous question."""
            st.session_state["current_index"] = st.session_state["current_index"] - 1

        if st.button("Previous", key="previous_button", on_click=_previous_callback):
            pass

    def drawNextButton(self) -> None:
        """Draws a button to go to the next question.

        The check whether the there is a previous question is done in drawNextButton
        """

        def _next_callback() -> None:
            """Changes the session_state to the session_state of the next question."""
            st.session_state["current_index"] = st.session_state["current_index"] + 1

        if st.button("Next", key="next_button", on_click=_next_callback):
            pass

    def drawQuiz(self) -> None:
        """Draws the elements of the quiz."""
        self.current_index = st.session_state.get("current_index", 0)
        QuestionDrawer.drawQuestion(self.question_list[self.current_index])
        col1, col2 = st.columns(2, gap=None, width=320)
        with col1:
            if self.current_index != 0:
                self.drawPreviousButton()

        with col2:
            if self.current_index != (len(self.question_list) - 1):
                self.drawNextButton()
