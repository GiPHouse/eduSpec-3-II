import os
from enum import Enum

import CreateForms
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


def determine_output_path(uploaded_file: UploadedFile) -> str:
    """Determines the output path

    Returns:
        str: returns the output path
    """
    output_path = "../data/"
    if uploaded_file.type == ".dx" or uploaded_file.type == ".jdx":
        output_path += "spectra/"
    elif uploaded_file.type == ".pdb" or uploaded_file.type == ".mol":
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


with st.form("baseform"):
    _options = [t.typestr for t in QuestionType]
    questionType = st.selectbox(
        label="Select the type of the question that you want to create", options=_options
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
        if uploaded_file is not None:
            os.makedirs("../data", exist_ok=True)
            output_path = determine_output_path(uploaded_file)
            with open(output_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File saved to {output_path}")
            st.session_state["last_successful_file"] = output_path

        st.session_state["last_successful_title"] = title
        st.session_state["last_successful_questionBody"] = questionBody
        st.session_state["last_successful_questionType"] = questionType
        st.success("Form submitted successfully.")

        CreateForms.decideAndCreateForm()
