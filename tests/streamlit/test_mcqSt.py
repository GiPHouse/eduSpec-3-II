from streamlit.testing.v1 import AppTest


def render_mcq_question() -> None:
    """Render a multiple choice question in a Streamlit test app."""
    from questions.MultipleChoiceQuestion import MultipleChoiceQuestion

    question = MultipleChoiceQuestion(
        "question1",
        "Example Question",
        "here's a question",
        ["a", "b", "c"],
        1,
        ["a: wrong", "b: correct", "c: wrong"],
    )
    question.drawYourself()


def test_mcq_renders_radio_and_options() -> None:
    """Test that the multiple choice question renders its radio input."""
    at = AppTest.from_function(render_mcq_question)
    at.run()

    assert not at.exception
    assert len(at.radio) == 1
    assert at.radio[0].label == "Pick one"
    assert list(at.radio[0].options) == ["a", "b", "c"]


def test_mcq_select_first_option() -> None:
    """Test selecting the first multiple choice option."""
    at = AppTest.from_function(render_mcq_question)
    at.run()

    assert not at.exception
    at.radio[0].set_value("a").run()

    assert at.radio[0].value == "a"


def test_mcq_select_middle_option() -> None:
    """Test selecting the middle multiple choice option."""
    at = AppTest.from_function(render_mcq_question)
    at.run()

    assert not at.exception
    at.radio[0].set_value("b").run()

    assert at.radio[0].value == "b"


def test_mcq_select_last_option() -> None:
    """Test selecting the last multiple choice option."""
    at = AppTest.from_function(render_mcq_question)
    at.run()

    assert not at.exception
    at.radio[0].set_value("c").run()

    assert at.radio[0].value == "c"
