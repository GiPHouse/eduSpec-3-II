import os
from abc import ABC, abstractmethod
from typing import Any, Optional

import streamlit as st

from MoleculeDisplay import MoleculeDisplay


class Question(ABC):
    """The general question class/interface.

    This contains both base attributes shared between question types,
    and a few interface functions that are unique to each.
    """

    def __init__(self, name: str, title: str, bodytext: str, imgpath: Optional[list[str]] = None):
        """Initialises a Question instance. DO NOT USE THE QUESTION CLASS DIRECTLY.

        Args:
            name (str): The unique name/ID of the question.
            title (str): The title of the question.
            bodytext (str): The body text of the question.
            imgpath (Optional[list[str]], optional): Paths to the images used for the question. Defaults to None.
        """
        self.name = name
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

    def drawImage(self) -> None:
        """Draw Image"""
        if self.imgpath is not None:
            for img_path in self.imgpath:
                if not img_path:
                    continue
                ext = os.path.splitext(img_path)[1].lower()
                if ext in [".pdb", ".ent"]:
                    MoleculeDisplay.drawYourself(img_path)
                else:
                    st.image(img_path)
