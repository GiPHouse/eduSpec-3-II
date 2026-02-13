from abc import ABC, abstractmethod
from typing import Any, Optional


class Question(ABC):
    """_summary_

    Args:
        ABC (_type_): _description_
    """

    def __init__(self, title: str, bodytext: str, imgpath: Optional[str] = None):
        """_summary_

        Args:
            title (str): _description_
            bodytext (str): _description_
            imgpath (Optional[str], optional): _description_. Defaults to None.
        """
        self.title = title
        self.bodytext = bodytext
        self.imgpath = imgpath

    @abstractmethod
    def verifyAndFeedback(self) -> tuple[bool, str]:
        """_summary_"""
        pass

    @abstractmethod
    def feedback(self) -> str:
        """_summary_"""
        pass

    @abstractmethod
    def drawYourself(self) -> Any:
        """_summary_"""
        pass
