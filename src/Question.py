from abc import ABC, abstractmethod
from typing import Any, Optional


class Question(ABC):
    """The general question class/interface.

    This contains both base attributes shared between question types,
    and a few interface functions that are unique to each.
    """

    def __init__(self, title: str, bodytext: str, imgpath: Optional[str] = None):
        """Initialises a Question instance. DO NOT USE THE QUESTION CLASS DIRECTLY.

        Args:
            title (str): The title of the question.
            bodytext (str): The body text of the question.
            imgpath (Optional[str], optional): Path to the image used for the question. Defaults to None.
        """
        self.title = title
        self.bodytext = bodytext
        self.imgpath = imgpath

    @abstractmethod
    def verifyAndFeedback(self) -> tuple[bool, str]:
        """Interface template. Returns whether an answer is correct and the feedback given."""
        pass

    @abstractmethod
    def feedback(self) -> str:
        """Interface template. Returns the feedback for an answer."""

    @abstractmethod
    def drawYourself(self) -> Any:
        """_summary_"""
        pass
