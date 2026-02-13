from typing import Optional

from Question import Question


class MultipleChoiceQuestion(Question):
    """_summary_

    Args:
        Question (_type_): _description_
    """

    def __init__(
        self,
        title: str,
        bodytext: str,
        answers: list[str],
        correct_answer: int,
        feedbacks: list[str],
        imgpath: Optional[str] = None,
    ):
        """_summary_

        Args:
            title (str): _description_
            bodytext (str): _description_
            answers (list[str]): _description_
            correct_answer (int): _description_
            feedbacks (list[str]): _description_
            imgpath (Optional[str], optional): _description_. Defaults to None.
        """
        assert len(answers) == len(feedbacks)
        assert correct_answer >= 0 and correct_answer < len(answers)

        super().__init__(title, bodytext, imgpath)
        print(self.bodytext)
        self.answers = answers
        self.correct_answer = correct_answer
        self.feedbacks = feedbacks

    def verifyAndFeedback(self, user_input: int) -> tuple[bool, str]:
        """_summary_

        Args:
            user_input (int): _description_

        Returns:
            (bool, str): _description_
        """
        return ((self.correct_answer == user_input), self.feedback(user_input))

    def feedback(self, user_input: int) -> str:
        """_summary_

        Args:
            user_input int: _description_

        Returns:
            str: _description_
        """
        return self.feedbacks[user_input]
