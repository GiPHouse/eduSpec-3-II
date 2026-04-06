from dataclasses import dataclass
from typing import Any, Optional

import streamlit as st

from pages.jsme_component import jsme_component
from questions.WordQuestion import WordQuestion


@dataclass(frozen=True)
class MoleculeDrawingConfig:
    """Configuration for a molecule drawing question.

    Attributes:
    expected_smiles (str):
        The canonical SMILES string that represents the correct answer.
        This is used to verify the student's drawing.

    seed_smiles (str):
        The initial SMILES string loaded into the editor when the question
        is rendered. Can be empty or an example structure.

    widget_key (str):
        Unique Streamlit key used to prevent duplicate widget conflicts
        when multiple molecule editors are rendered on the same page.(could be left empty if
        only one editor is used per page, but good practice to always set it)
    """

    expected_smiles: str  # what you want them to draw (answer)
    seed_smiles: str  # what editor starts with
    widget_key: str  # unique key for Streamlit widget


class MoleculeDrawingQuestion(WordQuestion):
    """A concrete implementation of a Question that allows users to draw a molecule using a JSME editor.

    The drawn molecule is captured as a SMILES string and compared
    against an expected SMILES answer for validation.

    Inherits from:
        Question: Abstract base class defining the question interface.
    """

    def __init__(
        self,
        name: str,
        title: str,
        bodytext: str,
        config: MoleculeDrawingConfig,
        feedbacks: list[str],
        imgpath: Optional[str] = None,
    ):
        """Initializes a MoleculeDrawingQuestion instance.

        Args:
        title (str):
            Title of the question.

        bodytext (str):
            The main prompt or instruction shown to the student.

        config (MoleculeDrawingConfig):
            Configuration object containing expected answer,
            initial editor state, and widget key.

        feedbacks (list[str]):
            The feedbacks to the answers.
            Needs to have 2 elements: correct feedback and incorrect feedback

        imgpath (Optional[str], optional):
            Optional path to an image associated with the question.
            Defaults to None.
        """
        super().__init__(
            name=name,
            title=title,
            bodytext=bodytext,
            imgpath=imgpath,
            correct_answer=config.expected_smiles.strip(),
            feedbacks=feedbacks,
        )

        self.widget_key = config.widget_key
        self.default = config.seed_smiles

        # internal key used to force-remount the JSME component
        self._nonce_key = f"{self.widget_key}__jsme_nonce"
        self._last_seen_key = f"{self.widget_key}__last_seen"

        if self._nonce_key not in st.session_state:
            st.session_state[self._nonce_key] = 0
        if self._last_seen_key not in st.session_state:
            st.session_state[self._last_seen_key] = self.default

        # store last drawn value here
        self._latest_smiles: Optional[str] = None

    def drawYourself(self) -> Optional[str]:
        """Renders the JSME molecule editor in the Streamlit interface.

        Captures the currently drawn molecule as a SMILES string and
        stores it internally for later validation.

        Returns:
            Optional[str]:
                The drawn SMILES string if available, otherwise None.
        """
        base_key = self.widget_key
        default_val = (self.default or "").strip()

        if base_key not in st.session_state:
            st.session_state[base_key] = default_val

        previous_base = (st.session_state.get(self._last_seen_key) or "").strip()
        current_base = (st.session_state.get(base_key) or "").strip()

        # Only treat it as a reset if the outside state changed
        # from a non-default value back to the default value.
        reset_requested = previous_base != default_val and current_base == default_val

        if reset_requested:
            st.session_state[self._nonce_key] += 1
            self._latest_smiles = None
            st.session_state[self._last_seen_key] = default_val
            st.rerun()

        nonce = st.session_state[self._nonce_key]
        component_key = f"{base_key}__jsme__{nonce}"

        data = jsme_component(default_smiles=self.default, key=component_key)

        smiles = ""
        if isinstance(data, dict):
            smiles = data.get("smiles", "").strip()

        if smiles:
            self._latest_smiles = smiles
            st.session_state[base_key] = smiles
            st.session_state[self._last_seen_key] = smiles
            return smiles

        self._latest_smiles = None
        st.session_state[self._last_seen_key] = current_base
        st.info("Draw a molecule in the editor, then click Submit Answer.")
        return None

    def verifyAndFeedback(
        self, user_input: Optional[str] = None, *args: Any, **kwargs: Any
    ) -> tuple[bool, str]:
        """Validates the submitted molecule against the expected answer.

        The method compares the drawn SMILES string with the expected
        SMILES stored in the configuration.

        Returns:
        tuple[bool, str]:
            A tuple where:
                - The first value indicates whether the answer is correct.
                - The second value contains feedback for the user.
        """
        submitted = (user_input or self._latest_smiles or "").strip()
        if not submitted:
            return False, "No SMILES found. Please draw a molecule first."

        # Delegate the actual comparison + feedback selection to WordQuestion
        return super().verifyAndFeedback(submitted)

        # Improve the incorrect message to include what they drew + what was expected
        # if not ok:
        #     expected = self.correct_answer  # set by WordQuestion
        #     return False, f"Incorrect. Expected {expected}, but you drew {submitted}."

        # return True, msg

    def feedback(self) -> str:
        """Provides default feedback for incorrect submissions.

        Returns:
            str:
                A generic feedback message encouraging retry.
        """
        return "Try again: make sure the structure matches the target molecule."

    """
    Template to create a question like this:
    st.set_page_config(page_title="Molecule Drawing Question")

    q = MoleculeDrawingQuestion(
        title="Draw ethanol",
        bodytext="Use the editor to draw ethanol and submit.",
        config=MoleculeDrawingConfig(
            expected_smiles="CCO",
            seed_smiles="",
            widget_key= "q1",
        ),
    )

    QuestionDrawer.drawQuestion(q)
    """
