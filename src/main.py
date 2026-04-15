import json
from pathlib import Path

import streamlit as st

import pages
from QuestionDrawer import QuestionDrawer
from questions.MoleculeDrawingQuestion import MoleculeDrawingConfig, MoleculeDrawingQuestion

# Get the absolute path to the data directory
data_dir = Path(__file__).parent.parent / "data"
pages_file = data_dir / "navigation" / "pages.json"

with open(pages_file) as f:
    PAGES = json.load(f)

# # Navigation session state
query_params = st.query_params

if "current_page" not in st.session_state:
    page_param = query_params.get("page")
    if page_param and page_param in PAGES:
        st.session_state.current_page = page_param
    else:
        st.session_state.current_page = "Home"

current_page = st.session_state.current_page
func_name = PAGES.get(current_page)


# Call the actual function dynamically
if func_name and hasattr(pages, func_name):
    getattr(pages, func_name)()  # call the function
else:
    st.error(f"Page '{current_page}' not found.")
# current_page = st.session_state.current_page
# page_function = PAGES[current_page]
# page_function()

# st.set_page_config(page_title="Molecule Drawing Question")

# q = MoleculeDrawingQuestion(
#     name="name",
#     title="Draw ethanol",
#     bodytext="Use the editor to draw ethanol and submit.",
#     config=MoleculeDrawingConfig(
#         expected_smiles="CCO",
#         seed_smiles="",
#         widget_key="q1",
#     ),
# )

# QuestionDrawer.drawQuestion(q)


# QuestionDrawer.drawQuestion(questionmult)
