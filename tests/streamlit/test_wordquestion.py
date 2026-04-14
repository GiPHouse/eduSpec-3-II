from streamlit.testing.v1 import AppTest

from QuestionDrawer import QuestionDrawer
from questions.WordQuestion import WordQuestion
from tests.streamlit.helpers import all_text_content, get_button_by_label


def make_question() -> WordQuestion:
    return WordQuestion(
        name="word1",
        title="Name The Molecule",
        bodytext="Type the common name for H2O.",
        correct_answer="water",
        feedbacks=["Nice work.", "Please try again."],
    )


def render_word_question() -> None:
    QuestionDrawer.drawQuestion(make_question())


def test_word_question_renders_prompt_and_input() -> None:
    at = AppTest.from_function(render_word_question)
    at.run()

    assert at.title[0].value == "Name The Molecule"
    assert "Type the common name for H2O." in all_text_content(at)
    assert len(at.text_input) == 1


def test_word_question_submit_correct_answer_shows_success() -> None:
    at = AppTest.from_function(render_word_question)
    at.run()

    at.text_input[0].input("water")
    get_button_by_label(at, "Submit Answer").click().run()

    assert "Your answer is correct!" in all_text_content(at)
    assert "Nice work." in all_text_content(at)


def test_word_question_submit_wrong_answer_shows_error() -> None:
    at = AppTest.from_function(render_word_question)
    at.run()

    at.text_input[0].input("steam")
    get_button_by_label(at, "Submit Answer").click().run()

    assert "Your answer is incorrect!" in all_text_content(at)
    assert "Please try again." in all_text_content(at)


def test_word_question_reset_restores_default_state() -> None:
    at = AppTest.from_function(render_word_question)
    at.session_state["word_input_Name The Molecule"] = "steam"
    at.run()

    get_button_by_label(at, "Reset").click().run()

    assert at.session_state["word_input_Name The Molecule"] == ""
