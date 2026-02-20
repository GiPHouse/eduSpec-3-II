import streamlit as st

from MoleculeDrawingQuestion import MoleculeDrawingConfig, MoleculeDrawingQuestion
from QuestionDrawer import QuestionDrawer


def main() -> None:
    """main"""
    st.set_page_config(page_title="Molecule Drawing Question")

    q = MoleculeDrawingQuestion(
        title="Draw ethanol",
        bodytext="Use the editor to draw ethanol and submit.",
        config=MoleculeDrawingConfig(
            expected_smiles="CCO",
            seed_smiles="CCO",
            widget_key="molecule_q1",
        ),
    )

    QuestionDrawer.drawQuestion(q)


if __name__ == "__main__":
    main()
