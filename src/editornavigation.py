import os

import streamlit as st

import editor.CreateForms as CreateForms
from editor.editor import QuestionType, determine_output_path, initialize_state

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
    if (
        not title.strip()
        or (not questionBody.strip())
        or (not question_id.strip())
        or (questionType == "Spectral Question" and (uploaded_file == []))
    ):
        st.error("Question ID, Title, Question Body are required.")
    else:
        st.session_state["question_submitted"] = False
        st.session_state["show_question_form"] = False
        st.session_state["overwrite_done"] = False
        spectral_counter = 0
        if uploaded_file is not None:
            st.session_state["last_successful_file"] = []

            for newFile in uploaded_file:
                os.makedirs("../data", exist_ok=True)
                output_path = determine_output_path(newFile)
                if output_path == f"../data/spectra/{newFile.name}":
                    spectral_counter += 1
                    st.session_state["last_successful_spectral_path"] = output_path
                else:
                    st.session_state["last_successful_file"].append(output_path)
                with open(output_path, "wb") as f:
                    f.write(newFile.getbuffer())
        if spectral_counter != 1 and questionType == "Spectral Question":
            st.error(f"You need exactly one spectral data file, you have {spectral_counter} files")
            print("boo")
        else:
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
