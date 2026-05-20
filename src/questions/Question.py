import os
from abc import ABC, abstractmethod
from typing import Any, Optional

import streamlit as st

from Checker import Checker
from MoleculeDisplay import MoleculeDisplay


class Question(ABC):
    """The general question class/interface.

    This contains both base attributes shared between question types,
    and a few interface functions that are unique to each.
    """

    def __init__(
        self,
        name: str,
        title: str,
        bodytext: str,
        checker: Optional[Checker] = None,
        figures: Optional[list[dict]] = None,
        body_format: str = "text",
        download_data: Optional[str] = None,
    ):
        """Initialises a Question instance. DO NOT USE THE QUESTION CLASS DIRECTLY.

        Args:
            name (str): The unique name/ID of the question.
            title (str): The title of the question.
            bodytext (str): The body text of the question.
            figures (Optional[list[dict]], optional): Paths to the images used for the question. Defaults to None.
            body_format (str, optional): Whether the body should be shown as normal text or LaTeX.
            download_data (Optional[str], optional): path to the data that can be downloaded with download button. Defaults to None.
        """
        if body_format not in ["text", "latex"]:
            raise ValueError("body_format must be either 'text' or 'latex'")

        self.name = name
        self.title = title
        self.bodytext = bodytext
        self.checker = checker
        self.figures = figures
        self.body_format = body_format
        self.download_data = download_data

    @abstractmethod
    def verifyAndFeedback(self) -> tuple[bool, str]:
        """Interface template. Returns whether an answer is correct and the feedback given."""
        pass

    @abstractmethod
    def drawYourself(self) -> Any:
        """_summary_"""
        pass

    def drawImage(self) -> None:
        """Draw Image"""
        col_counter = 0
        col1, col2 = st.columns([1, 1])
        if self.figures is not None:
            for figure in self.figures:
                if not figure:
                    continue
                if col_counter == 0:
                    with col1:
                        ext = os.path.splitext(figure["path"])[1].lower()
                        if ext in [".pdb", ".ent"]:
                            MoleculeDisplay.drawYourself(figure["path"])
                        else:
                            st.image(figure["path"], use_container_width=True)
                        st.markdown(figure["description"])
                else:
                    with col2:
                        ext = os.path.splitext(figure["path"])[1].lower()
                        if ext in [".pdb", ".ent"]:
                            MoleculeDisplay.drawYourself(figure["path"])
                        else:
                            st.image(figure["path"], use_container_width=True)
                        st.markdown(figure["description"])
                col_counter = (col_counter + 1) % 2
