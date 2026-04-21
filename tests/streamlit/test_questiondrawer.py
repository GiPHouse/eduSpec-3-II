from pathlib import Path
from typing import Any
from unittest.mock import Mock, patch

from QuestionDrawer import QuestionDrawer


class DummyContext:
    """Simple context manager used to mock Streamlit containers and forms."""

    def __enter__(self) -> "DummyContext":
        """Enter the context."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: Any,
    ) -> bool:
        """Exit the context without suppressing exceptions."""
        return False


class FakeQuestion:
    """Simple fake question object for QuestionDrawer tests."""

    def __init__(
        self,
        *,
        title: str = "Example Question",
        bodytext: str = "Example body",
        widget_key: str = "widget_key",
        default: Any = "default value",
        imgpath: str = "test.txt",
        user_input: Any = "student answer",
    ) -> None:
        """Initialise the fake question."""
        self.title = title
        self.bodytext = bodytext
        self.widget_key = widget_key
        self.default = default
        self.imgpath = imgpath
        self.user_input = user_input
        self.draw_image_called: bool = False
        self.verify_calls: list[Any] = []

    def drawImage(self) -> None:
        """Record that drawImage was called."""
        self.draw_image_called = True

    def drawYourself(self) -> Any:
        """Return the configured user input."""
        return self.user_input

    def verifyAndFeedback(self, user_input: Any) -> tuple[bool, str]:
        """Record verification input and return a successful response."""
        self.verify_calls.append(user_input)
        return True, "Looks good"


def test_evaluate_answer_shows_success_for_correct_answer() -> None:
    """evaluateAnswer should show success for a correct answer."""
    current_question = Mock()
    current_question.verifyAndFeedback.return_value = (True, "Nice work")

    with (
        patch("QuestionDrawer.st.success") as mock_success,
        patch("QuestionDrawer.st.error") as mock_error,
    ):
        QuestionDrawer.evaluateAnswer(current_question, "answer")

    assert current_question.verifyAndFeedback.call_count == 1
    assert current_question.verifyAndFeedback.call_args.args == ("answer",)
    assert mock_success.call_count == 1
    assert mock_success.call_args.args == ("Your answer is correct!  \n Nice work",)
    assert mock_error.call_count == 0


def test_evaluate_answer_shows_error_for_incorrect_answer() -> None:
    """evaluateAnswer should show error for an incorrect answer."""
    current_question = Mock()
    current_question.verifyAndFeedback.return_value = (False, "Try again")

    with (
        patch("QuestionDrawer.st.success") as mock_success,
        patch("QuestionDrawer.st.error") as mock_error,
    ):
        QuestionDrawer.evaluateAnswer(current_question, "wrong")

    assert current_question.verifyAndFeedback.call_count == 1
    assert current_question.verifyAndFeedback.call_args.args == ("wrong",)
    assert mock_error.call_count == 1
    assert mock_error.call_args.args == ("Your answer is incorrect!  \n Try again",)
    assert mock_success.call_count == 0


def test_evaluate_answer_accepts_zero_as_input() -> None:
    """evaluateAnswer should still evaluate input when it is zero."""
    current_question = Mock()
    current_question.verifyAndFeedback.return_value = (True, "Zero is valid")

    with patch("QuestionDrawer.st.success") as mock_success, patch("QuestionDrawer.st.error"):
        QuestionDrawer.evaluateAnswer(current_question, 0)

    assert current_question.verifyAndFeedback.call_count == 1
    assert current_question.verifyAndFeedback.call_args.args == (0,)
    assert mock_success.call_count == 1
    assert mock_success.call_args.args == ("Your answer is correct!  \n Zero is valid",)


def test_evaluate_answer_ignores_none_input() -> None:
    """evaluateAnswer should do nothing when input is None."""
    current_question = Mock()

    with (
        patch("QuestionDrawer.st.success") as mock_success,
        patch("QuestionDrawer.st.error") as mock_error,
    ):
        QuestionDrawer.evaluateAnswer(current_question, None)

    assert current_question.verifyAndFeedback.call_count == 0
    assert mock_success.call_count == 0
    assert mock_error.call_count == 0


def test_draw_question_renders_common_elements() -> None:
    """drawQuestion should render the common question elements."""
    current_question = FakeQuestion()

    with (
        patch("QuestionDrawer.st.container", return_value=DummyContext()),
        patch("QuestionDrawer.st.form", return_value=DummyContext()),
        patch("QuestionDrawer.st.title") as mock_title,
        patch("QuestionDrawer.st.text") as mock_text,
        patch("QuestionDrawer.st.form_submit_button", return_value=False) as mock_submit,
        patch("QuestionDrawer.st.button") as mock_button,
    ):
        QuestionDrawer.drawQuestion(current_question)

    assert current_question.draw_image_called is True
    assert mock_title.call_count == 1
    assert mock_title.call_args.args == ("Example Question",)
    assert mock_text.call_count == 1
    assert mock_text.call_args.args == ("Example body",)
    assert mock_submit.call_count == 1
    assert mock_submit.call_args.args == ("Submit Answer",)
    assert mock_submit.call_args.kwargs == {"key": "submit_button_form"}
    assert mock_button.call_count == 1
    assert mock_button.call_args.args == ("Reset",)
    assert "on_click" in mock_button.call_args.kwargs


def test_draw_question_submit_evaluates_answer_when_input_exists() -> None:
    """drawQuestion should evaluate the answer after submit when user input exists."""
    current_question = FakeQuestion(user_input="my answer")

    with (
        patch("QuestionDrawer.st.container", return_value=DummyContext()),
        patch("QuestionDrawer.st.form", return_value=DummyContext()),
        patch("QuestionDrawer.st.title"),
        patch("QuestionDrawer.st.text"),
        patch("QuestionDrawer.st.form_submit_button", return_value=True),
        patch("QuestionDrawer.st.button"),
        patch.object(QuestionDrawer, "evaluateAnswer") as mock_evaluate,
    ):
        QuestionDrawer.drawQuestion(current_question)

    assert mock_evaluate.call_count == 1
    assert mock_evaluate.call_args.args == (current_question, "my answer")


def test_draw_question_submit_does_not_evaluate_when_input_is_none() -> None:
    """drawQuestion should not evaluate the answer when user input is None."""
    current_question = FakeQuestion(user_input=None)

    with (
        patch("QuestionDrawer.st.container", return_value=DummyContext()),
        patch("QuestionDrawer.st.form", return_value=DummyContext()),
        patch("QuestionDrawer.st.title"),
        patch("QuestionDrawer.st.text"),
        patch("QuestionDrawer.st.form_submit_button", return_value=True),
        patch("QuestionDrawer.st.button"),
        patch.object(QuestionDrawer, "evaluateAnswer") as mock_evaluate,
    ):
        QuestionDrawer.drawQuestion(current_question)

    assert mock_evaluate.call_count == 0


def test_draw_question_reset_button_callback_restores_default() -> None:
    """drawQuestion reset callback should restore the widget key to the default value."""
    current_question = FakeQuestion(widget_key="reset_key", default="restored")
    fake_session_state: dict[str, Any] = {"reset_key": "changed"}
    stored_callback: dict[str, Any] = {}

    def fake_button(label: str, on_click: Any) -> None:
        """Capture the reset callback passed to st.button."""
        stored_callback["label"] = label
        stored_callback["callback"] = on_click
        return None

    with (
        patch("QuestionDrawer.st.container", return_value=DummyContext()),
        patch("QuestionDrawer.st.form", return_value=DummyContext()),
        patch("QuestionDrawer.st.title"),
        patch("QuestionDrawer.st.text"),
        patch("QuestionDrawer.st.form_submit_button", return_value=False),
        patch("QuestionDrawer.st.session_state", fake_session_state),
        patch("QuestionDrawer.st.button", side_effect=fake_button),
    ):
        QuestionDrawer.drawQuestion(current_question)

        assert stored_callback["label"] == "Reset"
        stored_callback["callback"]()
        assert fake_session_state["reset_key"] == "restored"


def test_draw_question_calls_draw_download_for_spectral_question() -> None:
    """drawQuestion should call _drawDownload for spectral questions."""

    class FakeSpectralQuestion(FakeQuestion):
        """Fake spectral question type."""

    current_question = FakeSpectralQuestion()

    with (
        patch("QuestionDrawer.SpectralQuestion", FakeSpectralQuestion),
        patch("QuestionDrawer.st.container", return_value=DummyContext()),
        patch("QuestionDrawer.st.form", return_value=DummyContext()),
        patch("QuestionDrawer.st.title"),
        patch("QuestionDrawer.st.text"),
        patch("QuestionDrawer.st.form_submit_button", return_value=False),
        patch("QuestionDrawer.st.button"),
        patch.object(QuestionDrawer, "_drawDownload") as mock_draw_download,
    ):
        QuestionDrawer.drawQuestion(current_question)

    assert mock_draw_download.call_count == 1
    assert mock_draw_download.call_args.args == (current_question,)


def test_draw_download_calls_streamlit_download_button(tmp_path: Path) -> None:
    """_drawDownload should call Streamlit's download_button with the correct arguments."""
    test_file = tmp_path / "spectrum.txt"
    test_file.write_text("example spectral data", encoding="utf-8")

    current_question = Mock()
    current_question.imgpath = str(test_file)

    with patch("QuestionDrawer.st.download_button") as mock_download_button:
        QuestionDrawer._drawDownload.__wrapped__(current_question)  # noqa: SLF001

    assert mock_download_button.call_count == 1
    assert mock_download_button.call_args.args[0] == "Download Spectral Data"
    assert mock_download_button.call_args.kwargs["file_name"] == "spectrum.txt"
    assert mock_download_button.call_args.kwargs["icon"] == ":material/file_download:"
