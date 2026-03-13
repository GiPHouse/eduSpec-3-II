import streamlit as st


def createIntegerQuestionForm() -> None:
    """_summary_"""
    pass


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
