from streamlit.testing.v1 import AppTest

SCRIPT_QUESTION_APP = """
from typing import Any

import streamlit as st

from questions.ScriptQuestion import ScriptQuestion


class FakeScript:
    \"\"\"Fake script used for Streamlit integration testing.\"\"\"

    def run(self, params: dict[str, Any]) -> dict[str, Any]:
        \"\"\"Return feedback based on the submitted parameters.\"\"\"
        number = params["number"]
        text = params["text"]
        choice = params["choice"]

        correct = number == 4 and text == "hello"

        return {
            "correct": correct,
            "feedback": "Correct answer." if correct else "Wrong answer.",
            "output": {
                "type": "markdown",
                "data": f"Output: number={number}, text={text}, choice={choice}",
            },
        }


question = ScriptQuestion(
    name="script_question",
    title="Script Question",
    bodytext="Fill in the parameters and submit.",
    script=FakeScript(),
    parameters=[
        {
            "name": "number",
            "label": "Number",
            "inputType": "integer",
            "default": 0,
        },
        {
            "name": "text",
            "label": "Text",
            "inputType": "text",
            "default": "",
        },
        {
            "name": "choice",
            "label": "Choice",
            "inputType": "select",
            "options": ["A", "B"],
            "default": "A",
        },
    ],
    body_format="text",
)

st.title(question.title)
st.write(question.bodytext)

values = question.drawYourself()

if st.button("Submit"):
    correct, feedback = question.verifyAndFeedback(values)

    if correct:
        st.success(feedback)
    else:
        st.error(feedback)

    question.drawFeedbackResult()
"""


def test_script_question_app_loads_without_errors() -> None:
    """Test that the ScriptQuestion Streamlit app loads."""
    app = AppTest.from_string(SCRIPT_QUESTION_APP).run()

    assert not app.exception
    assert app.title[0].value == "Script Question"
    assert len(app.number_input) == 1
    assert len(app.text_input) == 1
    assert len(app.selectbox) == 1
    assert len(app.button) == 1


def test_script_question_submit_shows_success_and_output() -> None:
    """Test that correct input shows success feedback and script output."""
    app = AppTest.from_string(SCRIPT_QUESTION_APP).run()

    app.number_input[0].set_value(4).run()
    app.text_input[0].set_value("hello").run()
    app.selectbox[0].set_value("B").run()
    app.button[0].click().run()

    assert not app.exception
    assert len(app.success) == 1
    assert "Correct answer." in app.success[0].value

    markdown_values = [markdown.value for markdown in app.markdown]
    assert any("Output: number=4, text=hello, choice=B" in value for value in markdown_values)


def test_script_question_submit_shows_error_for_wrong_answer() -> None:
    """Test that wrong input shows error feedback."""
    app = AppTest.from_string(SCRIPT_QUESTION_APP).run()

    app.number_input[0].set_value(2).run()
    app.text_input[0].set_value("hello").run()
    app.button[0].click().run()

    assert not app.exception
    assert len(app.error) == 1
    assert "Wrong answer." in app.error[0].value
