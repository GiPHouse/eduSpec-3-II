from checkers.BaseIntegerChecker import BaseIntegerChecker


class CustomIntegerChecker(BaseIntegerChecker):
    """Default/example integer checker"""

    def buildSelf(self, obj: dict) -> None:
        """Builds the checker.

        Args:
            obj (dict):
        """
        self.lower_bound = obj.get("lowerBound")
        self.upper_bound = obj.get("upperBound")
        self.lower_feedback = obj.get("lowerFeedback")
        self.higher_feedback = obj.get("higherFeedback")
        self.correct_feedback = obj.get("correctFeedback")

        assert isinstance(self.lower_bound, int)
        assert isinstance(self.upper_bound, int)
        assert isinstance(self.lower_feedback, str)
        assert isinstance(self.higher_feedback, str)
        assert isinstance(self.correct_feedback, str)

    def serialiseSelf(self) -> dict:
        """Generates a dictionary with all the arguments for `IntegerChecker`

        Returns:
            dict: The dictionary, ready to be turned into json

            The dict includes the following values:
            - lowerBound (int): The lowest correct answer
            - upperBound (int): The highest correct answer
            - lowerFeedback (string): The feedback given when the answer is below the lower bound
            - correctFeedback (string): The feedback given when the answer is correct
            - higherFeedback (string): The feedback given when the answer is above he upper bound
        """
        return {
            "lowerBound": self.lower_bound,
            "upperBound": self.upper_bound,
            "lowerFeedback": self.lower_feedback,
            "correctFeedback": self.correct_feedback,
            "higherFeedback": self.higher_feedback,
        }

    def checkInteger(self, answer: int) -> tuple[bool, str]:
        """Check whether the answer to an integer question is correct.

        Args:
            answer (int): The answer to check.

        Returns:
            tuple[bool, str]: Whether the answer is correct, and the feedback to give.
        """
        if answer < self.lower_bound:
            return (False, self.lower_feedback)
        elif answer > self.upper_bound:
            return (False, self.higher_feedback)
        else:
            return (True, self.correct_feedback)
