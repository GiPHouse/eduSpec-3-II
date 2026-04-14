from streamlit.testing.v1 import AppTest

from QuestionDrawer import QuestionDrawer
from questions.IntegerQuestion import IntegerQuestion
from tests.streamlit.helpers import all_text_content, get_button_by_label


def make_question() -> IntegerQuestion:
    return IntegerQuestion(
        name="int1",
        title="Count Protons",
        bodytext="Enter the proton count for carbon.",
        correct_answer=(6, 6),
        feedbacks=["Exactly right.", "Too small.", "Too large."],
    )


def render_integer_question() -> None:
    QuestionDrawer.drawQuestion(make_question())


def test_integer_question_renders_prompt_and_number_input() -> None:
    at = AppTest.from_function(render_integer_question)
    at.run()

    assert at.title[0].value == "Count Protons"
    assert "Enter the proton count for carbon." in all_text_content(at)
    assert len(at.number_input) == 1


def test_integer_question_submit_correct_answer_shows_success() -> None:
    at = AppTest.from_function(render_integer_question)
    at.run()

    at.number_input[0].set_value(6)
    get_button_by_label(at, "Submit Answer").click().run()

    assert "Your answer is correct!" in all_text_content(at)
    assert "Exactly right." in all_text_content(at)


def test_integer_question_submit_large_answer_shows_error() -> None:
    at = AppTest.from_function(render_integer_question)
    at.run()

    at.number_input[0].set_value(8)
    get_button_by_label(at, "Submit Answer").click().run()

    assert "Your answer is incorrect!" in all_text_content(at)
    assert "Too large." in all_text_content(at)


def test_integer_question_reset_restores_default_state() -> None:
    at = AppTest.from_function(render_integer_question)
    at.session_state["number_input_Count Protons"] = 8
    at.run()

    get_button_by_label(at, "Reset").click().run()

    assert at.session_state["number_input_Count Protons"] is None
