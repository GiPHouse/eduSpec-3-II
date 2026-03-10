import streamlit as st

from Question import Question
from QuestionDrawer import QuestionDrawer


class Quiz:
    """Class to create the elements of a quiz."""

    def __init__(self, name: str, question_list: list[Question]) -> None:
        """Initialises a quiz instance.

        Args:
            name (str): The unique name/id of the quiz.
            question_list (list[Question]): A list of questions in the quiz.
        """
        self.name = name
        if "current_index" not in st.session_state:
            st.session_state["current_index"] = 0
        self.current_index = 0
        self.question_list = question_list
        # Use quiz name in the key so each quiz has its own index
        if f"current_index_{self.name}" not in st.session_state:
            st.session_state[f"current_index_{self.name}"] = 0
        self.current_index = st.session_state[f"current_index_{self.name}"]

    def drawQuestionNavigator(self) -> None:
        """Draws numbered boxes at the bottom to navigate between questions."""
        if not self.question_list:
            return

        st.divider()

        BUTTONS_PER_ROW = 10

        chunks = [
            self.question_list[i:i + BUTTONS_PER_ROW]
            for i in range(0, len(self.question_list), BUTTONS_PER_ROW)
        ]

        button_index = 0
        for chunk in chunks:
            cols = st.columns(BUTTONS_PER_ROW)
            for _, col in enumerate(cols[:len(chunk)]):
                with col:
                    button_type = "primary" if button_index == self.current_index else "secondary"
                    if st.button(
                        str(button_index + 1),
                        key=f"question_nav_{self.name}_{button_index}",
                        type=button_type,
                        width='stretch',
                    ):
                        st.session_state[f"current_index_{self.name}"] = button_index
                        st.rerun()
                button_index += 1

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
        self.current_index = st.session_state.get(f"current_index_{self.name}", 0)
        safe_index = min(self.current_index, len(self.question_list) - 1)
        QuestionDrawer.drawQuestion(self.question_list[safe_index])
        self.drawQuestionNavigator()
