"""ananbacin4"""

import streamlit as st

from MoleculeQuestion import MoleculeQuestion
from QuestionDrawer import QuestionDrawer


def main() -> None:
    """main

    tbd

    """
    st.set_page_config(page_title="Molecule Question", layout="centered")

    # Create a MoleculeQuestion (integrated into your Question system)
    question = MoleculeQuestion(
        title="Draw Alanine",
        bodytext="Draw alanine and submit the SMILES.",
        imgpath=None,
        question_id="q1",
        answers_path="answers.csv",
        seed_smiles="N[CH](C)C(=O)O",
    )

    # Use your existing QuestionDrawer
    QuestionDrawer.drawQuestion(question)


if __name__ == "__main__":
    main()
