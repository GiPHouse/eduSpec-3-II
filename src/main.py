import streamlit as st
import pandas as pd

from MultipleChoiceQuestion import MultipleChoiceQuestion
from QuestionDrawer import QuestionDrawer
from MoleculeDisplay import MoleculeDisplay

st.write("""
Hello world
""")

mcq = MultipleChoiceQuestion("hi",["aaa","bbb"],0,["true","false"])
QuestionDrawer.drawQuestion(mcq)

# 3D Molecule Display Section
st.divider()
st.header("3D Molecule Viewer")

# Example 1: Display protein by PDB ID
st.subheader("Protein Structure (PDB: 1CRN)")
MoleculeDisplay.displayProteinById(pdb_id='1CRN', style='stick', height=500, width=800)
MoleculeDisplay.displayMoleculeFromFile('src/neoNR8.pdb', style='stick', height=500, width=800)
# Example 2: Display molecule from PDB string (water molecule)
