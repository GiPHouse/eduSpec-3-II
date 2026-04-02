import streamlit as st

from managers.QuestionManager import QuestionManager
from questions.IntegerQuestion import IntegerQuestion


def createIntegerQuestionForm() -> None:
    """_summary_"""
    with st.form("IntegerQuestionForm"):
        IQ_correct_range = st.slider(
            "Please choose the correct range",
            min_value=-1000.0,
            max_value=1000.0,
            value=(-50.0, 50.0),
            key="IntegerQuestion_correct_range",
        )
        IQ_correct_feedback = st.text_input(
            "Please specify the feedback when the answer is within range",
            key="IntegerQuestion_correct_feedback",
        )
        IQ_lower_feedback = st.text_input(
            "Please specify the feedback when the answer is lower than range",
            key="IntegerQuestion_lower_feedback",
        )
        IQ_higher_feedback = st.text_input(
            "Please specify the feedback when the answer is higher than range",
            key="IntegerQuestion_higher_feedback",
        )
        IQsubmitButton = st.form_submit_button()

    if IQsubmitButton:
        new_question = IntegerQuestion(
            "some_question",
            st.session_state["last_successful_title"],
            st.session_state["last_successful_questionBody"],
            IQ_correct_range,
            [IQ_correct_feedback, IQ_lower_feedback, IQ_higher_feedback],
            st.session_state.get("last_successful_file", None),
        )
        try:
            QuestionManager.saveQuestion(new_question)
            st.success(f"Question {new_question.title} created!")
        except Exception as e:
            st.error(f"An error occurred during saving:{e}")


def createWordQuestionForm() -> None:
    """_summary_"""
    st.write("boo")


def createMultipleChoiceQuestionForm() -> None:
    """_summary_"""
    pass


def createSpectralQuestionForm() -> None:
    """_summary_"""
    pass


def createDrawingQuestionForm() -> None:
    """_summary_"""
    pass


def decideAndCreateForm() -> None:
    """_summary_"""
    # Now, we want to dinamically create a form based on the question type.
    if "last_successful_questionType" in st.session_state:
        match st.session_state["last_successful_questionType"]:
            case "Integer Question":
                createIntegerQuestionForm()

            case "Word Question":
                createWordQuestionForm()

            case "MultipleCoice":
                createMultipleChoiceQuestionForm()

            case "Spectral Question":
                createSpectralQuestionForm()

            case "Drawing Question":
                createDrawingQuestionForm()
    else:
        print("AA")
