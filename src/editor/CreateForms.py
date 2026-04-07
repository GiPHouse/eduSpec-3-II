import streamlit as st

from managers.QuestionManager import QuestionManager
from QuestionDrawer import QuestionDrawer
from questions.IntegerQuestion import IntegerQuestion
from questions.MoleculeDrawingQuestion import MoleculeDrawingConfig, MoleculeDrawingQuestion
from questions.MultipleChoiceQuestion import MultipleChoiceQuestion
from questions.Question import Question
from questions.SpectralQuestion import SpectralQuestion
from questions.WordQuestion import WordQuestion


def createIntegerQuestionForm() -> None:
    """Function that creates a form so that user can specify an Integer Question"""
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

        col1, col2 = st.columns(2)
        with col1:
            IQsubmitButton = st.form_submit_button()
        with col2:
            IQPreviewButton = st.form_submit_button(key="prevbut_IQ", label="Preview")

    if IQsubmitButton:
        new_question = IntegerQuestion(
            st.session_state["last_successful_id"],
            st.session_state["last_successful_title"],
            st.session_state["last_successful_questionBody"],
            IQ_correct_range,
            [IQ_correct_feedback, IQ_lower_feedback, IQ_higher_feedback],
            st.session_state.get("last_successful_file", None),
        )
        try:
            QuestionManager.saveQuestion(new_question)

            st.session_state["show_question_form"] = False
            st.session_state["question_submitted"] = True

            st.rerun()
        except FileExistsError:
            if not st.session_state["overwrite_done"]:
                handle_same_id(new_question)
        except Exception as e:
            st.error(f"An error occurred during saving:{e}")
    if IQPreviewButton:
        new_question = IntegerQuestion(
            st.session_state["last_successful_id"],
            st.session_state["last_successful_title"],
            st.session_state["last_successful_questionBody"],
            IQ_correct_range,
            [IQ_correct_feedback, IQ_lower_feedback, IQ_higher_feedback],
            st.session_state.get("last_successful_file", None),
        )
        preview_question(new_question)
    if st.session_state["overwrite_done"]:
        st.session_state["show_question_form"] = False
        st.session_state["question_submitted"] = True


def createWordQuestionForm() -> None:
    """Function that creates a form so that user can specify a Word Question"""
    with st.form("WordQuestionForm"):
        WQ_correct_answer = st.text_input(
            "Please specify the correct answer", key="WordQuestion_correct_answer"
        )
        WQ_correct_feedback = st.text_input(
            "Please specify the feedback when the answer is correct",
            key="WordQuestion_correct_feedback",
        )
        WQ_wrong_feedback = st.text_input(
            "Please specify the feedback when the answer is incorrect",
            key="WordQuestion_wrong_feedback",
        )
        col1, col2 = st.columns(2)
        with col1:
            WQ_submit_button = st.form_submit_button()
        with col2:
            WQ_preview_button = st.form_submit_button(key="wq_prevbut", label="Preview")
    if WQ_submit_button:
        new_question = WordQuestion(
            st.session_state["last_successful_id"],
            st.session_state["last_successful_title"],
            st.session_state["last_successful_questionBody"],
            WQ_correct_answer,
            [WQ_correct_feedback, WQ_wrong_feedback],
            st.session_state.get("last_successful_file", None),
        )
        try:
            QuestionManager.saveQuestion(new_question)

            st.session_state["show_question_form"] = False
            st.session_state["question_submitted"] = True

            st.rerun()
        except FileExistsError:
            if not st.session_state["overwrite_done"]:
                handle_same_id(new_question)
        except Exception as e:
            st.error(f"An error occurred during saving:{e}")
    if WQ_preview_button:
        new_question = WordQuestion(
            st.session_state["last_successful_id"],
            st.session_state["last_successful_title"],
            st.session_state["last_successful_questionBody"],
            WQ_correct_answer,
            [WQ_correct_feedback, WQ_wrong_feedback],
            st.session_state.get("last_successful_file", None),
        )
        preview_question(new_question)
    if st.session_state["overwrite_done"]:
        st.session_state["show_question_form"] = False
        st.session_state["question_submitted"] = True


def createMultipleChoiceQuestionForm() -> None:
    """Function that creates a form so that user can specify a Multiple Choice Question"""
    MCQ_choice_count = st.number_input(
        "Please specify the number of choices this question offers",
        key="MCQ_choice_count",
        step=1,
        min_value=1,
        max_value=10,
    )
    MCQ_correct_answer = st.number_input(
        "Please specify index of the choice with correct answer (starting from 1)",
        key="mcq_correct_answer",
        step=1,
        min_value=1,
        max_value=MCQ_choice_count,
    )

    if MCQ_choice_count > 0:
        with st.form("MultipleChoiceQuestionForm"):
            answers = []
            feedbacks = []
            for i in range(MCQ_choice_count):
                st.markdown(f"**Choice {i + 1}**")
                st.text_input(
                    f"Answer {i + 1}",
                    key=f"mcq_answer_{i}",
                    placeholder=f"Enter answer option {i + 1}",
                )
                st.text_input(
                    f"Feedback for answer {i + 1}",
                    key=f"mcq_feedback_{i}",
                    placeholder=f"Enter feedback for answer option {i + 1}",
                )
            col1, col2 = st.columns(2)
            with col1:
                MCQ_submit_button = st.form_submit_button(key="mcq_submit")
            with col2:
                MCQ_previous_button = st.form_submit_button(key="mcq_prevbut", label="Preview")

        if MCQ_submit_button:
            answers = [st.session_state[f"mcq_answer_{i}"] for i in range(MCQ_choice_count)]
            feedbacks = [st.session_state[f"mcq_feedback_{i}"] for i in range(MCQ_choice_count)]
            new_question = MultipleChoiceQuestion(
                st.session_state["last_successful_id"],
                st.session_state["last_successful_title"],
                st.session_state["last_successful_questionBody"],
                answers,
                (MCQ_correct_answer - 1),
                feedbacks,
                st.session_state.get("last_successful_file", None),
            )
            try:
                QuestionManager.saveQuestion(new_question)

                st.session_state["show_question_form"] = False
                st.session_state["question_submitted"] = True

                st.rerun()
            except FileExistsError:
                if not st.session_state["overwrite_done"]:
                    handle_same_id(new_question)
            except Exception as e:
                st.error(f"An error occurred during saving:{e}")
        if MCQ_previous_button:
            answers = [st.session_state[f"mcq_answer_{i}"] for i in range(MCQ_choice_count)]
            feedbacks = [st.session_state[f"mcq_feedback_{i}"] for i in range(MCQ_choice_count)]
            new_question = MultipleChoiceQuestion(
                st.session_state["last_successful_id"],
                st.session_state["last_successful_title"],
                st.session_state["last_successful_questionBody"],
                answers,
                (MCQ_correct_answer - 1),
                feedbacks,
                st.session_state.get("last_successful_file", None),
            )
            preview_question(new_question)

    else:
        st.error("Number of choices must be at least 1.")
    if st.session_state["overwrite_done"]:
        st.session_state["show_question_form"] = False
        st.session_state["question_submitted"] = True


def createSpectralQuestionForm() -> None:
    """Function that creates a form so that user can specify a Spectral Question"""
    with st.form("SpectralQuestionForm"):
        SQ_correct_answer = st.number_input(
            "Please specify the correct value (This can be the y-value of a peak, regardless of the unit)",
            key="SQ_correct_answer",
        )
        SQ_tolerance = st.number_input(
            "Please specify if you want to accept the answer with a tolerance (if you want to accept answers that are a bit off)",
            key="SQ_tolerance",
        )

        SQ_correct_feedback = st.text_input(
            "Please specify the feedback when the answer is within acceptable range",
            key="SQ_correct_feedback",
        )
        SQ_incorrect_feedback = st.text_input(
            "Please specify the feedback when the answer is wrong",
            key="SQ_lower_feedback",
        )
        col1, col2 = st.columns(2)
        with col1:
            SQsubmitButton = st.form_submit_button()
        with col2:
            SQpreviousButton = st.form_submit_button(key="SQ_prevbut", label="Preview")
    if SQsubmitButton:
        new_question = SpectralQuestion(
            st.session_state["last_successful_id"],
            st.session_state["last_successful_title"],
            st.session_state["last_successful_questionBody"],
            st.session_state.get("last_successful_file", None),
            SQ_correct_answer,
            [SQ_correct_feedback, SQ_incorrect_feedback],
            SQ_tolerance,
        )
        try:
            QuestionManager.saveQuestion(new_question)

            st.session_state["show_question_form"] = False
            st.session_state["question_submitted"] = True

            st.rerun()
        except FileExistsError:
            if not st.session_state["overwrite_done"]:
                handle_same_id(new_question)
        except Exception as e:
            st.error(f"An error occurred during saving:{e}")
    if SQpreviousButton:
        new_question = SpectralQuestion(
            st.session_state["last_successful_id"],
            st.session_state["last_successful_title"],
            st.session_state["last_successful_questionBody"],
            st.session_state.get("last_successful_file", None),
            SQ_correct_answer,
            [SQ_correct_feedback, SQ_incorrect_feedback],
            SQ_tolerance,
        )
        preview_question(new_question)
    if st.session_state["overwrite_done"]:
        st.session_state["show_question_form"] = False
        st.session_state["question_submitted"] = True


def createDrawingQuestionForm() -> None:
    """Function that creates a form so that user can specify a Molecule Drawing Question"""
    with st.form("DrawingQuestionForm"):
        DQ_correct_answer = st.text_input(
            "Please specify the correct answer in SMILES form", key="DQ_correct"
        )
        DQ_default_answer = st.text_input(
            "Please specify if you want the students to start from a base molecule, in SMILES form (can be empty)",
            key="DQ_default",
        )
        DQ_correct_feedback = st.text_input(
            "Please specify the feedback when the answer is correct",
            key="DQ_correct_feedback",
        )
        DQ_wrong_feedback = st.text_input(
            "Please specify the feedback when the answer is wrong",
            key="DQ_wrong_feedback",
        )

        col1, col2 = st.columns(2)
        with col1:
            DQsubmitButton = st.form_submit_button()
        with col2:
            DQPreviewButton = st.form_submit_button(key="prevbut_DQ", label="Preview")

        if DQsubmitButton:
            config = MoleculeDrawingConfig(
                expected_smiles=DQ_correct_answer,
                seed_smiles=DQ_default_answer,
                widget_key="dq_default_widget_key",
            )
            new_question = MoleculeDrawingQuestion(
                st.session_state["last_successful_id"],
                st.session_state["last_successful_title"],
                st.session_state["last_successful_questionBody"],
                config=config,
                feedbacks=[DQ_correct_feedback, DQ_wrong_feedback],
                imgpath=st.session_state.get("last_successful_file", None),
            )
            try:
                QuestionManager.saveQuestion(new_question)

                st.session_state["show_question_form"] = False
                st.session_state["question_submitted"] = True

                st.rerun()
            except FileExistsError:
                if not st.session_state["overwrite_done"]:
                    handle_same_id(new_question)
            except Exception as e:
                st.error(f"An error occurred during saving:{e}")
        if DQPreviewButton:
            config = MoleculeDrawingConfig(
                expected_smiles=DQ_correct_answer,
                seed_smiles="C",
                widget_key="dq_default_widget_key",
            )
            new_question = MoleculeDrawingQuestion(
                st.session_state["last_successful_id"],
                st.session_state["last_successful_title"],
                st.session_state["last_successful_questionBody"],
                config=config,
                feedbacks=[DQ_correct_feedback, DQ_wrong_feedback],
                imgpath=st.session_state.get("last_successful_file", None),
            )
            preview_question(new_question)
        if st.session_state["overwrite_done"]:
            st.session_state["show_question_form"] = False
            st.session_state["question_submitted"] = True


def decideAndCreateForm() -> None:
    """A function that maps chosen question types to corresponding forms to create that specific question."""
    # Now, we want to dinamically create a form based on the question type.
    if "last_successful_questionType" in st.session_state:
        match st.session_state["last_successful_questionType"]:
            case "Integer Question":
                createIntegerQuestionForm()

            case "Word Question":
                createWordQuestionForm()

            case "Multiple Choice Question":
                createMultipleChoiceQuestionForm()

            case "Spectral Question":
                createSpectralQuestionForm()

            case "Drawing Question":
                createDrawingQuestionForm()
    else:
        st.error("An error has occurred, the editor cannot interpret this form.")


@st.dialog("Preview of described question, press the top-right button to close this menu")
def preview_question(question: Question) -> None:
    """Opens a new "window" and draws the given question there. The question is independent from any quiz logic, so it's a preview

    Args:
        question (Question): The question that it displays
    """
    QuestionDrawer.drawQuestion(question)


@st.dialog("A choice must be done")
def handle_same_id(new_question: Question) -> None:
    """Handles the situation when the user creates a question with an existing id. Gives the user two choices: Overwrite or Cancel.

    Args:
        new_question (_type_): The candidate question that user just specified.
    """
    # Now, we know that user wanted to write a question but another question with the same ID exists.
    st.text(
        "There exists another question with the same ID. You can choose to overwrite it or go back from top-right button"
    )
    st.text("You can preview both questions here, and make your choice")
    col1, col2 = st.columns(2)

    with col1:
        preview_existing_q = st.button(label="Preview Existing Question", key="existing_prevbut")
    with col2:
        preview_new_q = st.button(label="Preview New Question", key="new_prevbut")
    overwrite = st.button(label="Overwrite", key="overwrite_but")
    if preview_existing_q:
        try:
            QuestionDrawer.drawQuestion(
                QuestionManager.loadQuestion(st.session_state["last_successful_id"])
            )
        except Exception as e:
            st.error(f"An error has occurred, please start over:{e}")
    if preview_new_q:
        QuestionDrawer.drawQuestion(new_question)
    if overwrite:
        QuestionManager.updateQuestion(new_question)
        st.session_state["overwrite_done"] = True
        st.session_state["show_question_form"] = False
        st.session_state["question_submitted"] = True
        st.rerun()
