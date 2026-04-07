# Yes, I hate this as much as anyone.
# Yes, it does fix your import errors instantly
# No, it should not be kept
# import editor.editor  # noqa: F401

import os
from enum import Enum
from pathlib import Path

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from editor.CreateForms import decideAndCreateForm


def initialize_state() -> None:
    """Initializes the session state flags that are used to ensure control flow."""
    defaults = {
        "show_question_form": False,
        "question_submitted": False,
        "last_successful_title": "",
        "last_successful_questionBody": "",
        "last_successful_questionType": None,
        "last_successful_file": None,
        "overwrite_done": False,
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def determine_output_path(uploaded_file: UploadedFile) -> str:
    """Determines the output path

    Returns:
        str: returns the output path
    """
    output_path = "../data/"
    extension = Path(uploaded_file.name).suffix.lower()
    if extension == ".dx" or extension == ".jdx":
        output_path += "spectra/"
    elif extension == ".pdb" or extension == ".mol":
        output_path += "molecules/"
    else:
        output_path += "images/"
    output_path += f"{uploaded_file.name}"
    return output_path


class QuestionType(Enum):
    """Question type enum

    Args:
        Enum (_type_): I dont know what to put here tbh.
    """

    INTEGER = "Integer Question"
    WORD = "Word Question"
    MULTIPLECHOICE = "Multiple Choice Question"
    SPECTRAL = "Spectral Question"
    DRAWING = "Drawing Question"

    def __init__(self, typestr: str):
        """init

        Args:
            typestr (str): The string to show in the form
        """
        self.typestr = typestr


initialize_state()
with st.form("baseform"):
    _options = [t.typestr for t in QuestionType]
    questionType = st.selectbox(
        label="Select the type of the question that you want to create", options=_options
    )
    question_id = st.text_input(
        "ID (This helps you identify the question)",
        placeholder="Please specify an ID for the question",
        key="idfield",
    )
    title = st.text_input("Title", placeholder="Put in the title of the question", key="titlefield")
    questionBody = st.text_area(
        "Question Body", placeholder="Put in the body of the question", key="bodyfield"
    )
    uploaded_file = st.file_uploader("Choose a file")

    submitButton = st.form_submit_button()

if submitButton:
    if not title.strip() or not questionBody.strip():
        st.error("Title and Question Body are required.")
    else:
        st.session_state["question_submitted"] = False

        if uploaded_file is not None:
            os.makedirs("../data", exist_ok=True)
            output_path = determine_output_path(uploaded_file)
            with open(output_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File saved to {output_path}")
            st.session_state["last_successful_file"] = output_path
        st.session_state["last_successful_id"] = question_id
        st.session_state["last_successful_title"] = title
        st.session_state["last_successful_questionBody"] = questionBody
        st.session_state["last_successful_questionType"] = questionType
        st.session_state["show_question_form"] = True
        st.success("Form submitted successfully.")

        st.rerun()

if st.session_state.get("show_question_form") and not st.session_state.get("question_submitted"):
    decideAndCreateForm()
if st.session_state.get("question_submitted"):
    st.success("Question created!")
