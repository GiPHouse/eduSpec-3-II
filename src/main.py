import streamlit as st

from MoleculeDrawingQuestion import MoleculeDrawingConfig, MoleculeDrawingQuestion
from QuestionDrawer import QuestionDrawer

st.set_page_config(page_title="Molecule Drawing Question")

q = MoleculeDrawingQuestion(
    name="name",
    title="Draw ethanol",
    bodytext="Use the editor to draw ethanol and submit.",
    config=MoleculeDrawingConfig(
        expected_smiles="CCO",
        seed_smiles="",
        widget_key="q1",
    ),
)

QuestionDrawer.drawQuestion(q)


# QuestionDrawer.drawQuestion(questionmult)
