from typing import Optional

import streamlit as st

from questions.Question import Question


class WordQuestion(Question):
    """Word question"""

    def __init__(
        self,
        name: str,
        title: str,
        bodytext: str,
        correct_answer: str,
        feedbacks: list[str],
        imgpath: Optional[str] = None,
    ):
        """Initializes word question

        Args:
            name (str): The unique name/ID of the question.
            title (str): The title of the question
            bodytext (str): The body text of the question
            correct_answer str: The correct answer as a string
            feedbacks (list[str]): The feedbacks to the answers. Needs to have 2 elements: correct feedback and incorrect feedback
            imgpath (Optional[str], optional): Represents the image if there is one, Defaults to None.
        """
        super().__init__(name, title, bodytext, imgpath)
        self.correct_answer = correct_answer
        self.feedbacks = feedbacks
        self.widget_key = f"word_input_{title}"
        self.default = ""

    def verifyAndFeedback(self, user_input: str) -> tuple[bool, str]:
        """checks if input is correct

        Args:
            user_input (str): answer of the user

        Returns:
            (bool, str): return a tuple with whether the answer is correct and its corresponding feedback
        """
        isAnswerCorrect: bool
        ReturnFeedback: str

        if user_input == self.correct_answer:
            isAnswerCorrect = True
            ReturnFeedback = self.feedbacks[0]
        else:
            isAnswerCorrect = False
            ReturnFeedback = self.feedbacks[1]

        return (isAnswerCorrect, ReturnFeedback)

    def feedback(self) -> None:
        """Unused, all logic is in `verifyAndFeedback()`"""
        pass

    def drawYourself(self) -> Optional[str]:
        """Question draws itself

        Returns:
            Optional[str]: returns the user input
        """
        if self.widget_key not in st.session_state:
            st.session_state[self.widget_key] = self.default

        answer = st.text_input(
            "enter the right answer:",
            value=None,
            key=self.widget_key,
        )
        if answer is not None and answer.strip() != "":
            return answer
        return None
