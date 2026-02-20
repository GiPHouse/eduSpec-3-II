"""anan2

Returns:
_type_: _description_
"""

from typing import Optional, Tuple

import streamlit as st

from AnswerChecker import AnswerChecker
from MoleculeDrawer import MoleculeDrawer, MoleculeDrawerConfig
from Question import Question


class MoleculeQuestion(Question):
    """A Question type that uses JSME to let the user draw a molecule. Fully compatible with your existing QuestionDrawer.

    tbd
    """

    def __init__(
        self,
        title: str,
        bodytext: str,
        imgpath: Optional[str],
        question_id: str,
        answers_path: str = "answers.csv",
        seed_smiles: str = "N[CH](C)C(=O)O",
    ):
        """init

        Args:
            title (str): _description_
            bodytext (str): _description_
            imgpath (Optional[str]): _description_
            question_id (str): _description_
            answers_path (str, optional): _description_. Defaults to "answers.csv".
            seed_smiles (str, optional): _description_. Defaults to "N[CH](C)C(=O)O".
        """
        # Initialize base Question
        super().__init__(title=title, bodytext=bodytext, imgpath=imgpath)

        self.question_id = question_id
        self.answers_path = answers_path
        self.seed_smiles = seed_smiles

        # Required for your Reset logic
        self.widget_key = f"molecule_{self.question_id}"
        self.default = self.seed_smiles

        # Cache AnswerChecker in session_state
        cache_key = f"_answer_checker__{self.answers_path}"
        if cache_key not in st.session_state:
            st.session_state[cache_key] = AnswerChecker(self.answers_path)

        self._checker: AnswerChecker = st.session_state[cache_key]

        self._drawer = MoleculeDrawer(
            MoleculeDrawerConfig(
                default_smiles=self.seed_smiles,
                show_output_box=True,
            )
        )

    # -------------------------------------------------
    # Required abstract methods from Question
    # -------------------------------------------------

    def drawYourself(self) -> str:
        """overloaded question drawer

        Returns:
            str: _description_
        """
        current_seed = st.session_state.get(self.widget_key, self.seed_smiles)
        self._drawer.config.default_smiles = current_seed
        return self._drawer.render(key=self.widget_key)

    def verifyAndFeedback(self, user_input: Optional[str]) -> Tuple[bool, str]:
        """overloaded verifier

        Args:
            user_input (Optional[str]): _description_

        Returns:
            Tuple[bool, str]: _description_
        """
        if user_input is None or not user_input.strip():
            return False, "No SMILES submitted. Draw a molecule first."

        result = self._checker.check(self.question_id, user_input)

        if result.is_correct:
            return True, "Correct! Your SMILES matches an accepted answer."

        if result.accepted:
            accepted_preview = "\n".join(result.accepted[:5])
            return False, "Incorrect.\n\nAccepted answer(s):\n" + accepted_preview

        return False, f"No answer found for id '{self.question_id}'."

    def feedback(self) -> None:
        """feedback if necessary

        Returns:
            _type_: _description_
        """
        return None
