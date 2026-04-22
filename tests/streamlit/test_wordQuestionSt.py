from streamlit.testing.v1 import AppTest


def render_word_question() -> None:
    """Render a word question in a Streamlit test app."""
    from questions.WordQuestion import WordQuestion

    question = WordQuestion(
        "question1",
        "Example Question",
        "here's a question",
        "The correct answer",
        ["correct", "wrong"],
    )
    question.drawYourself()


def test_word_question_renders_text_input() -> None:
    """Test that the word question renders its text input."""
    at = AppTest.from_function(render_word_question)
    at.run()

    assert not at.exception
    assert len(at.text_input) == 1
    assert at.text_input[0].label == "enter the right answer:"


def test_word_question_accepts_input() -> None:
    """Test that the word question accepts typed input."""
    at = AppTest.from_function(render_word_question)
    at.run()

    assert not at.exception
    at.text_input[0].set_value("My answer").run()

    assert at.text_input[0].value == "My answer"


def test_word_question_accepts_correct_input() -> None:
    """Test that the word question accepts the correct answer."""
    at = AppTest.from_function(render_word_question)
    at.run()

    assert not at.exception
    at.text_input[0].set_value("The correct answer").run()

    assert at.text_input[0].value == "The correct answer"


def test_word_question_accepts_empty_input() -> None:
    """Test that the word question allows empty input."""
    at = AppTest.from_function(render_word_question)
    at.run()

    assert not at.exception
    at.text_input[0].set_value("").run()

    assert at.text_input[0].value == ""
