from collections.abc import Callable
from typing import Any


class Checker:
    """Wrapper class for custom checkers"""

    def __init__(self, checking_function: Callable, checking_file_name: str) -> None:
        """Initialises a checker object

        Args:
            checking_function (function): The function that will be used for checking.
            checking_file_name (str): The filename that the checker originated from.
        """
        self.checking_function = checking_function
        self.file_name = checking_file_name

    def get_file_name(self) -> str:
        """Returns the filename that the checker originated from.

        Returns:
            str: The file name.
        """
        return self.file_name

    def check(self, answer: Any) -> tuple[bool, str]:
        """Check whether an answer is correct.

        Args:
            answer (Any): The answer to check.

        Returns:
            tuple[bool, str]: Whether it is correct, and the feedback.
        """
        return self.checking_function(answer)
