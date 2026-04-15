import os
from enum import Enum
from pathlib import Path

import CreateForms  # VScode gives a warning for this but I guess it works?
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


def initialize_state(reset: bool = False) -> None:
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
        if (k not in st.session_state) or reset:
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
        os.makedirs("../data/spectra", exist_ok=True)
    elif extension == ".pdb" or extension == ".mol":
        output_path += "molecules/"
        os.makedirs("../data/molecules", exist_ok=True)
    else:
        output_path += "images/"
        os.makedirs("../data/images", exist_ok=True)
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
with st.form("baseform", enter_to_submit=False):
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
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["jpg", "jpeg", "png", "dx", "jdx", "pdb", "mol"],
        max_upload_size=10,
        accept_multiple_files=True,
    )

    submitButton = st.form_submit_button()

if submitButton:
    if not title.strip() or not questionBody.strip() or not question_id.strip():
        st.error("Question ID, Title, Question Body are required.")
    else:
        st.session_state["question_submitted"] = False
        st.session_state["show_question_form"] = False
        st.session_state["overwrite_done"] = False

        if uploaded_file is not None:
            st.session_state["last_successful_file"] = []
            for newFile in uploaded_file:
                os.makedirs("../data", exist_ok=True)
                output_path = determine_output_path(newFile)
                with open(output_path, "wb") as f:
                    f.write(newFile.getbuffer())
                st.success(f"File saved to {output_path}")
                st.session_state["last_successful_file"].append(output_path)
        st.session_state["last_successful_id"] = question_id
        st.session_state["last_successful_title"] = title
        st.session_state["last_successful_questionBody"] = questionBody
        st.session_state["last_successful_questionType"] = questionType
        st.session_state["show_question_form"] = True
        st.success("Form submitted successfully.")

        st.rerun()

if st.session_state.get("show_question_form") and not st.session_state.get("question_submitted"):
    CreateForms.decideAndCreateForm()
if st.session_state.get("question_submitted"):
    st.success("Question created!")
    initialize_state(reset=True)
    # st.rerun()
