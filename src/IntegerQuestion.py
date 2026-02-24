from typing import Optional

import streamlit as st

from Question import Question


class IntegerQuestion(Question):
    """Integer question"""

    def __init__(
        self,
        title: str,
        bodytext: str,
        correct_answer: tuple[int, int],
        feedbacks: list[str],
        imgpath: Optional[str] = None,
    ):
        """Initializes integer question

        Args:
            title (str): The title of the question
            bodytext (str): The body text of the question
            correct_answer tuple[int, int]: The range in which the answer is correct
            feedbacks (list[str]): The feedbacks to the answers. Needs to have 3 elements: [right answer, too small answer, too big answer]
            imgpath (Optional[str], optional): Represents the image if there is one, Defaults to None.
        """
        # feedbacks is as follows: [feedback for right answer, feedback for too small answer, feedback for too large answer]
        assert correct_answer[0] <= correct_answer[1]
        assert len(feedbacks) == 3

        super().__init__(title, bodytext, imgpath)
        print(self.bodytext)
        self.correct_answer = correct_answer
        self.feedbacks = feedbacks
        self.widget_key = f"number_input_{title}"
        self.default = 0

    def verifyAndFeedback(self, user_input: int) -> tuple[bool, str]:
        """checks if input is correct

        Args:
            user_input (int): answer of the user

        Returns:
            (bool, str): return a tuple with whether the ansewr is correct and its corresponding feedback
        """
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

    def feedback(self) -> None:
        """does nothing currently"""
        pass

    def drawYourself(self) -> int:
        """Question draws itself

        Returns:
            int: returns the user input
        """
        if self.widget_key not in st.session_state:
            st.session_state[self.widget_key] = self.default

        number = st.number_input(
            "enter the right number:",
            step=1,
            placeholder="",
            key=self.widget_key,
        )
        return number
