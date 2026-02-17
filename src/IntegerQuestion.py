from typing import Optional

import streamlit as st

from Question import Question


class IntegerQuestion(Question):
    """_summary_

    Args:
        Question (_type_): _description_
    """

    def __init__(
        self,
        title: str,
        bodytext: str,
        correct_answer: tuple[int, int],
        feedbacks: list[str],
        imgpath: Optional[str] = None,
    ):
        """_summary_

        Args:
            title (str): _description_
            bodytext (str): _description_
            correct_answer (tuple[int, int]): _description_
            feedbacks (list[str]): _description_
            imgpath (Optional[str], optional): _description_. Defaults to None.
        """
        # the correct integer should be in the range between the first and second int, given as a tuple
        # feedbacks is as follows: [feedback for right answer, feedback for too small answer, feedback for too large answer]
        assert correct_answer[0] <= correct_answer[1]
        assert len(feedbacks) == 3

        super().__init__(title, bodytext, imgpath)
        print(self.bodytext)
        self.correct_answer = correct_answer
        self.feedbacks = feedbacks
        self.widget_key = "number_input"
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
