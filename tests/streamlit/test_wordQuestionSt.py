from streamlit.testing.v1 import AppTest


def render_word_question() -> None:
    """Render a word question in a Streamlit test app."""
    from QuestionDrawer import QuestionDrawer
    from questions.WordQuestion import WordQuestion

    question = WordQuestion(
        name="q1",
        title="Word Question",
        bodytext="Type the answer.",
        figures=[{"path": "data/images/test.png", "description": "This is a description!!"}],
        body_format="text",
        correct_answer="answer",
        feedbacks=["Correct!", "Incorrect!"],
    )
    QuestionDrawer.drawQuestion(question)


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


def test_word_question_renders_image_description() -> None:
    """Test that the word question renders the description of an image"""
    at = AppTest.from_function(render_word_question)
    at.run()

    assert not at.exception
    assert any(markdown.value == "This is a description!!" for markdown in at.markdown)


def test_word_question_renders_image() -> None:
    """Test that the word question renders an image element."""
    at = AppTest.from_function(render_word_question)
    at.run()

    assert not at.exception

    images = at.get("imgs")
    assert len(images) >= 1
