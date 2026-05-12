import os
from enum import Enum
from pathlib import Path

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
