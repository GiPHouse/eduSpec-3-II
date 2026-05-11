import os

import streamlit as st

import editor.CreateForms as CreateForms
from editor.editor import QuestionType, determine_output_path

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

    submitButton = st.form_submit_button("Next")


if submitButton or "last_successful_title" in st.session_state:
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
        # st.success("Form submitted successfully.")

        CreateForms.decideAndCreateForm()
