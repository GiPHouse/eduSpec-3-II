from streamlit.testing.v1 import AppTest

from QuestionDrawer import QuestionDrawer
from questions.MultipleChoiceQuestion import MultipleChoiceQuestion
from tests.streamlit.helpers import all_text_content, get_button_by_label


def make_question() -> MultipleChoiceQuestion:
    return MultipleChoiceQuestion(
        name="mcq1",
        title="Atomic Number",
        bodytext="Which option is the atomic number of oxygen?",
        answers=["6", "8", "10"],
        correct_answer=1,
        feedbacks=["Too low.", "Correct.", "Too high."],
    )


def render_multiple_choice_question() -> None:
    QuestionDrawer.drawQuestion(make_question())


def test_multiple_choice_question_renders_options() -> None:
    at = AppTest.from_function(render_multiple_choice_question)
    at.run()

    assert at.title[0].value == "Atomic Number"
    assert "Which option is the atomic number of oxygen?" in all_text_content(at)
    assert at.radio[0].options == ["6", "8", "10"]


def test_multiple_choice_question_submit_correct_answer_shows_success() -> None:
    at = AppTest.from_function(render_multiple_choice_question)
    at.run()

    at.radio[0].set_value("8")
    get_button_by_label(at, "Submit Answer").click().run()

    assert "Your answer is correct!" in all_text_content(at)
    assert "Correct." in all_text_content(at)


def test_multiple_choice_question_submit_wrong_answer_shows_error() -> None:
    at = AppTest.from_function(render_multiple_choice_question)
    at.run()

    at.radio[0].set_value("10")
    get_button_by_label(at, "Submit Answer").click().run()

    assert "Your answer is incorrect!" in all_text_content(at)
    assert "Too high." in all_text_content(at)


def test_multiple_choice_question_reset_restores_default_state() -> None:
    at = AppTest.from_function(render_multiple_choice_question)
    at.session_state["multiple_choice_Atomic Number"] = "10"
    at.run()

    get_button_by_label(at, "Reset").click().run()

    assert at.session_state["multiple_choice_Atomic Number"] is None
