from typing import Optional

import streamlit as st

from questions.Question import Question


class MultipleChoiceQuestion(Question):
    """Multiple-choice questions."""

    def __init__(
        self,
        name: str,
        title: str,
        bodytext: str,
        answers: list[str],
        correct_answer: int,
        feedbacks: list[str],
        imgpath: Optional[str] = None,
    ):
        """Initialises a new multiple-choice question

        Args:
            name (str): The unique name/ID of the question.
            title (str): The title of the questio
            bodytext (str): The body text of the question
            answers (list[str]): The possible answers
            correct_answer (int): The correct answer, as an index to the answers list
            feedbacks (list[str]): The feedbacks to the answers. Needs to be the same length as answers.
            imgpath (Optional[str], optional): Represents the image if there is one, Defaults to None.
        """
        assert len(answers) == len(feedbacks)
        assert correct_answer >= 0
        assert correct_answer < len(answers)

        super().__init__(name, title, bodytext, imgpath)
        self.answers = answers
        self.correct_answer = correct_answer
        self.feedbacks = feedbacks
        self.widget_key = f"multiple_choice_{title}"
        self.default = None

    def verifyAndFeedback(self, user_input: int) -> tuple[bool, str]:
        """Returns whether an answer is correct and the feedback given.

        Args:
            user_input (int): The chosen answer, as index to the answers.

        Returns:
            tuple[bool, str]: Whether the answer was correct, and the feedback.
        """
        return ((self.correct_answer == user_input), self.feedback(user_input))

    def feedback(self, user_input: int) -> str:
        """Returns the feedback for an answer.

        Args:
            user_input (_type_): The chosen answer, as index to the answers.

        Returns:
            str: The feedback for the chosen answer.
        """
        return self.feedbacks[user_input]

    def drawYourself(self) -> Optional[int]:
        """Question draws itself

        Returns:
            Optional[int]: returns the user input
        """
        # Options (Radio in streamlit)
        if self.widget_key not in st.session_state:
            st.session_state[self.widget_key] = self.default

        selected_option = st.radio(
            "Pick one", self.answers, index=self.default, key=self.widget_key
        )
        if selected_option is not None:
            selected_index = self.answers.index(selected_option)
            return selected_index
