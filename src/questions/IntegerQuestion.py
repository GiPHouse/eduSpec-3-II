from typing import Optional

import streamlit as st

from Checker import Checker
from questions.Question import Question


class IntegerQuestion(Question):
    """Integer question"""

    def __init__(
        self,
        name: str,
        title: str,
        bodytext: str,
        correct_answer: tuple[int | float, int | float],
        feedbacks: list[str],
        checker: Optional[Checker] = None,
        figures: Optional[list[dict]] = None,
        body_format: str = "text",
    ):
        """Initializes integer question

        Args:
            name (str): The unique name/ID of the question.
            title (str): The title of the question
            bodytext (str): The body text of the question
            correct_answer (tuple[int|float, int|float]): The range in which the answer is correct
            feedbacks (list[str]): The feedbacks to the answers. Needs to have 3 elements: [right answer, too small answer, too big answer]
            figures (Optional[list[dict]], optional): Represents the image if there is one, Defaults to None.
        """
        # feedbacks is as follows: [feedback for correct answer, feedback for too small answer, feedback for too large answer]

        super().__init__(name, title, bodytext, checker, figures, body_format)
        self.correct_answer = correct_answer
        self.feedbacks = feedbacks
        self.widget_key = f"number_input_{title}"
        self.default = None

    def verifyAndFeedback(self, user_input: int | float) -> tuple[bool, str]:
        """checks if input is correct

        Args:
            user_input (int|float): answer of the user

        Returns:
            (bool, str): return a tuple with whether the answer is correct and its corresponding feedback
        """
        if self.checker is not None:
            return self.checker.check(user_input)

        isAnswerCorrect: bool
        ReturnFeedback: str

        if user_input < self.correct_answer[0]:
            isAnswerCorrect = False
            ReturnFeedback = self.feedbacks[1]
        elif user_input > self.correct_answer[1]:
            isAnswerCorrect = False
            ReturnFeedback = self.feedbacks[2]
        else:
            isAnswerCorrect = True
            ReturnFeedback = self.feedbacks[0]

        return (isAnswerCorrect, ReturnFeedback)

    def drawYourself(self) -> Optional[int | float]:
        """Question draws itself

        Returns:
            Optional[int | float]: returns the user input
        """
        if self.widget_key not in st.session_state:
            st.session_state[self.widget_key] = self.default

        number = st.number_input(
            "enter the right number:",
            value=None,
            step=1 if isinstance(self.correct_answer[0], int) else 0.5,
            key=self.widget_key,
        )
        return number
