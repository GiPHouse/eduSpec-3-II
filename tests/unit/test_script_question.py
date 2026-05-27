from typing import Any
from unittest.mock import MagicMock, patch

from questions.ScriptQuestion import ScriptQuestion


def make_script_question(
    script: MagicMock | None = None,
    parameters: list[dict[str, Any]] | None = None,
) -> ScriptQuestion:
    """Create a ScriptQuestion for tests."""
    script_object = script if script is not None else MagicMock()

    return ScriptQuestion(
        name="script_question",
        title="Script Question",
        bodytext="Enter parameters.",
        script=script_object,
        parameters=parameters if parameters is not None else [],
        body_format="text",
    )


def test_draw_yourself_collects_values_from_all_supported_inputs() -> None:
    """Test that drawYourself reads values from all supported input widgets."""
    parameters = [
        {
            "name": "count",
            "label": "Count",
            "inputType": "integer",
            "default": 2,
        },
        {
            "name": "ratio",
            "label": "Ratio",
            "inputType": "number",
            "default": 1.5,
        },
        {
            "name": "level",
            "label": "Level",
            "inputType": "slider",
            "min": 1,
            "max": 10,
            "default": 3,
            "step": 1,
        },
        {
            "name": "enabled",
            "label": "Enabled",
            "inputType": "checkbox",
            "default": True,
        },
        {
            "name": "choice",
            "label": "Choice",
            "inputType": "select",
            "options": ["a", "b"],
            "default": "b",
        },
        {
            "name": "notes",
            "label": "Notes",
            "inputType": "textarea",
            "default": "hello",
        },
        {
            "name": "username",
            "label": "Username",
            "inputType": "text",
            "default": "student",
        },
    ]

    question = make_script_question(parameters=parameters)

    with (
        patch("questions.ScriptQuestion.st.number_input", side_effect=[2, 1.5]),
        patch("questions.ScriptQuestion.st.slider", return_value=3),
        patch("questions.ScriptQuestion.st.checkbox", return_value=True),
        patch("questions.ScriptQuestion.st.selectbox", return_value="b"),
        patch("questions.ScriptQuestion.st.text_area", return_value="hello"),
        patch("questions.ScriptQuestion.st.text_input", return_value="student"),
    ):
        values = question.drawYourself()

    assert values == {
        "count": 2,
        "ratio": 1.5,
        "level": 3,
        "enabled": True,
        "choice": "b",
        "notes": "hello",
        "username": "student",
    }


def test_verify_and_feedback_runs_script_and_stores_output() -> None:
    """Test that verifyAndFeedback runs the script and stores script output."""
    script = MagicMock()
    script.run.return_value = {
        "correct": False,
        "feedback": "Try again.",
        "output": {"type": "text", "data": "extra output"},
    }

    question = make_script_question(script=script)

    correct, feedback = question.verifyAndFeedback({"x": 1})

    script.run.assert_called_once_with({"x": 1})
    assert correct is False
    assert feedback == "Try again."
    assert question.last_script_output == {"type": "text", "data": "extra output"}


def test_verify_and_feedback_uses_default_correct_and_feedback_values() -> None:
    """Test that missing correct and feedback fields get safe defaults."""
    script = MagicMock()
    script.run.return_value = {}

    question = make_script_question(script=script)

    correct, feedback = question.verifyAndFeedback({"x": 1})

    assert correct is True
    assert feedback == ""
    assert question.last_script_output is None


def test_verify_and_feedback_handles_script_error() -> None:
    """Test that script execution errors become incorrect feedback."""
    script = MagicMock()
    script.run.side_effect = RuntimeError("boom")

    question = make_script_question(script=script)

    correct, feedback = question.verifyAndFeedback({"x": 1})

    assert correct is False
    assert feedback == "The script could not run: boom"
    assert question.last_script_output is None


def test_verify_and_feedback_rejects_non_boolean_correct_field() -> None:
    """Test that correct must be a boolean."""
    script = MagicMock()
    script.run.return_value = {"correct": "yes", "feedback": "ok"}

    question = make_script_question(script=script)

    correct, feedback = question.verifyAndFeedback({"x": 1})

    assert correct is False
    assert feedback == "The script result field 'correct' must be a boolean."
    assert question.last_script_output is None


def test_verify_and_feedback_rejects_non_string_feedback_field() -> None:
    """Test that feedback must be a string."""
    script = MagicMock()
    script.run.return_value = {"correct": True, "feedback": ["not", "a", "string"]}

    question = make_script_question(script=script)

    correct, feedback = question.verifyAndFeedback({"x": 1})

    assert correct is False
    assert feedback == "The script result field 'feedback' must be a string."
    assert question.last_script_output is None


def test_draw_feedback_result_draws_markdown_output() -> None:
    """Test that markdown script output is rendered as markdown."""
    question = make_script_question()
    question.last_script_output = {"type": "markdown", "data": "**hello**"}

    with (
        patch("questions.ScriptQuestion.st.divider") as divider_mock,
        patch("questions.ScriptQuestion.st.markdown") as markdown_mock,
    ):
        question.drawFeedbackResult()

    divider_mock.assert_called_once_with()
    markdown_mock.assert_called_once_with("**hello**")


def test_draw_feedback_result_draws_json_output() -> None:
    """Test that json script output is rendered as json."""
    question = make_script_question()
    question.last_script_output = {"type": "json", "data": {"x": 1}}

    with (
        patch("questions.ScriptQuestion.st.divider") as divider_mock,
        patch("questions.ScriptQuestion.st.json") as json_mock,
    ):
        question.drawFeedbackResult()

    divider_mock.assert_called_once_with()
    json_mock.assert_called_once_with({"x": 1})


def test_draw_feedback_result_does_nothing_without_output() -> None:
    """Test that no Streamlit output is drawn when there is no script output."""
    question = make_script_question()
    question.last_script_output = None

    with patch("questions.ScriptQuestion.st.divider") as divider_mock:
        question.drawFeedbackResult()

    divider_mock.assert_not_called()


def test_reset_session_state_resets_parameter_values() -> None:
    """Test that resetSessionState restores widget values to defaults."""
    parameters = [
        {"name": "count", "default": 5},
        {"name": "text_value", "default": "hello"},
        {"name": "without_default"},
    ]
    question = make_script_question(parameters=parameters)

    session_state = {
        "script_question_count": 99,
        "script_question_text_value": "changed",
        "script_question_without_default": "changed",
    }

    with patch("questions.ScriptQuestion.st.session_state", session_state):
        question.resetSessionState()

    assert session_state["script_question_count"] == 5
    assert session_state["script_question_text_value"] == "hello"
    assert session_state["script_question_without_default"] == ""
