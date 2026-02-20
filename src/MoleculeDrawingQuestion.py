from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

import streamlit as st

from pages.jsme_component import jsme_component
from Question import Question


@dataclass(frozen=True)
class MoleculeDrawingConfig:
    """dataclass for molecule drawing questions"""

    expected_smiles: str  # what you want them to draw (answer)
    seed_smiles: str  # what editor starts with
    widget_key: str  # unique key for Streamlit widget


class MoleculeDrawingQuestion(Question):
    """MOlecule Drawing Question

    Args:
        Question (_type_): _description_
    """

    def __init__(
        self,
        title: str,
        bodytext: str,
        config: MoleculeDrawingConfig,
        imgpath: Optional[str] = None,
    ):
        """_summary_

        Args:
            title (str): _description_
            bodytext (str): _description_
            config (MoleculeDrawingConfig): _description_
            imgpath (Optional[str], optional): _description_. Defaults to None.
        """
        super().__init__(title=title, bodytext=bodytext, imgpath=imgpath)
        self._cfg = config

        self.widget_key = self._cfg.widget_key
        self.default = self._cfg.seed_smiles

        # store last drawn value here
        self._latest_smiles: Optional[str] = None

    def drawYourself(self) -> Optional[str]:
        """Draws the editor and returns the current SMILES (or None).

        Also stores it so verifyAndFeedback() can access it later.

        Returns:
            Optional[str]: _description_
        """
        data = jsme_component(default_smiles=self.default, key=self.widget_key)

        smiles = ""
        if isinstance(data, dict):
            smiles = data.get("smiles", "").strip()

        if smiles:
            self._latest_smiles = smiles
            st.subheader("Your SMILES")
            st.code(smiles)
            return smiles

        self._latest_smiles = None
        st.info("Draw a molecule in the editor, then click Submit Answer.")
        return None

    def verifyAndFeedback(self, *args: Any, **kwargs: Any) -> tuple[bool, str]:
        """checking the answer.

        Returns:
            tuple[bool, str]: _description_
        """
        submitted = self._latest_smiles
        expected = self._cfg.expected_smiles.strip()

        if not submitted:
            return False, "No SMILES found. Please draw a molecule first."

        if submitted.strip() == expected:
            return True, f"Correct! Expected {expected}."

        return False, f"Incorrect. Expected {expected}, but you drew {submitted}."

    def feedback(self) -> str:
        """default feedback.

        Returns:
            str: _description_
        """
        return "Try again: make sure the structure matches the target molecule."
