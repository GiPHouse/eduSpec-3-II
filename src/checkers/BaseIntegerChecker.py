from abc import abstractmethod
from typing import final

from checkers.BaseChecker import BaseChecker, CheckerTypes


class BaseIntegerChecker(BaseChecker):
    """The base template for all integer question checkers. All integer checkers should be a subclass of this."""

    @final
    def configureAvailableQuestions(self) -> None:
        """Configures the checker to support integer questions"""
        super().configureAvailableQuestions()
        self._supported_questions.add(CheckerTypes.INTEGER)

    @abstractmethod
    def checkInteger(self, answer: int) -> tuple[bool, str]:
        """Checks whether an integer answer is correct.

        Args:
            answer (int): The answer given

        Returns:
            tuple[bool, str]: Whether it is correct, and the feedback it requires.
        """
        pass
