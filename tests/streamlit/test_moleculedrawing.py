from collections.abc import Iterator
from typing import Any
from unittest.mock import patch

import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest

from questions.MoleculeDrawingQuestion import (
    MoleculeDrawingConfig,
    MoleculeDrawingQuestion,
)

EXPECTED = "CCO"
WIDGET_KEY = "q1"


@pytest.fixture(autouse=True)
def clear_streamlit_state() -> Iterator[None]:
    """Clear Streamlit session state before and after each test."""
    st.session_state.clear()
    yield
    st.session_state.clear()


def make_question(
    *,
    expected_smiles: str = EXPECTED,
    seed_smiles: str = "",
    widget_key: str = WIDGET_KEY,
) -> MoleculeDrawingQuestion:
    """Create a molecule drawing question instance for tests."""
    return MoleculeDrawingQuestion(
        name="q1",
        title="Draw ethanol",
        bodytext="Use the editor to draw ethanol and submit.",
        config=MoleculeDrawingConfig(
            expected_smiles=expected_smiles,
            seed_smiles=seed_smiles,
            widget_key=widget_key,
        ),
        feedbacks=["Your answer is correct!", "Your answer is incorrect!"],
        figures=None,
        body_format="text",
    )


def render_molecule_question() -> None:
    """Render the molecule drawing question in a Streamlit test app."""
    from QuestionDrawer import QuestionDrawer
    from questions.MoleculeDrawingQuestion import (
        MoleculeDrawingConfig,
        MoleculeDrawingQuestion,
    )

    q = MoleculeDrawingQuestion(
        name="q1",
        title="Draw ethanol",
        bodytext="Use the editor to draw ethanol and submit.",
        config=MoleculeDrawingConfig(
            expected_smiles="CCO",
            seed_smiles="",
            widget_key="q1",
        ),
        feedbacks=["Your answer is correct!", "Your answer is incorrect!"],
        figures=None,
        body_format="text",
    )

    QuestionDrawer.drawQuestion(q)


def get_button_by_label(at: AppTest, label: str) -> Any:
    """Return the first button whose label matches the given text."""
    for button in at.button:
        if button.label == label:
            return button

    raise AssertionError(f"Button with label '{label}' was not found.")


def all_text_content(at: AppTest) -> str:
    """Collect visible text-like content from the rendered app."""
    parts = []

    for group in (
        at.title,
        at.text,
        at.markdown,
        at.info,
        at.success,
        at.error,
    ):
        parts.extend(str(x.value) for x in group)

    return " ".join(parts)


def test_verify_correct_smiles() -> None:
    """Check that the correct SMILES string is accepted."""
    q = make_question()

    ok, msg = q.verifyAndFeedback("CCO")

    assert ok is True
    assert "correct" in msg.lower()
    assert "incorrect" not in msg.lower()


def test_verify_incorrect_smiles_returns_incorrect_feedback() -> None:
    """Check that an incorrect SMILES string is rejected."""
    q = make_question()

    ok, msg = q.verifyAndFeedback("CCC")

    assert ok is False
    assert "incorrect" in msg.lower()


def test_verify_empty_smiles_returns_error() -> None:
    """Check that an empty SMILES string returns an error message."""
    q = make_question()

    ok, msg = q.verifyAndFeedback("")

    assert ok is False
    assert "No SMILES found" in msg


def test_whitespace_only_input_is_treated_as_empty() -> None:
    """Check that whitespace-only input is treated as empty."""
    q = make_question()

    ok, msg = q.verifyAndFeedback("   ")

    assert ok is False
    assert "No SMILES found" in msg


def test_constructor_sets_basic_fields() -> None:
    """Check that constructor values are stored correctly."""
    q = make_question(seed_smiles="C")

    assert q.widget_key == WIDGET_KEY
    assert q.default == "C"
    assert q.correct_answer == EXPECTED


def test_constructor_creates_internal_session_keys() -> None:
    """Check that constructor creates the internal Streamlit keys."""
    make_question()

    assert f"{WIDGET_KEY}__jsme_nonce" in st.session_state
    assert f"{WIDGET_KEY}__last_seen" in st.session_state


def test_draw_yourself_returns_component_smiles() -> None:
    """Check that drawYourself returns the SMILES from the component."""
    q = make_question()

    with patch(
        "questions.MoleculeDrawingQuestion.jsme_component",
        return_value={"smiles": "CCO"},
    ):
        result = q.drawYourself()

    assert result == "CCO"
    assert st.session_state[WIDGET_KEY] == "CCO"
    assert st.session_state[f"{WIDGET_KEY}__last_seen"] == "CCO"


def test_draw_yourself_without_smiles_shows_info() -> None:
    """Check that drawYourself shows info when no molecule is drawn."""
    q = make_question()

    with (
        patch(
            "questions.MoleculeDrawingQuestion.jsme_component",
            return_value=None,
        ),
        patch("questions.MoleculeDrawingQuestion.st.info") as mock_info,
    ):
        result = q.drawYourself()

    assert result is None
    mock_info.assert_called_once_with("Draw a molecule in the editor, then click Submit Answer.")


def test_app_renders_title_prompt_and_buttons() -> None:
    """Check that the app renders the title, prompt, and buttons."""
    at = AppTest.from_function(render_molecule_question)

    with patch(
        "questions.MoleculeDrawingQuestion.jsme_component",
        return_value=None,
    ):
        at.run()

    assert len(at.exception) == 0
    assert len(at.title) == 1
    assert at.title[0].value == "Draw ethanol"

    text = all_text_content(at)
    assert "Use the editor to draw ethanol and submit." in text
    assert "Draw a molecule in the editor" in text

    labels = [button.label for button in at.button]
    assert "Submit Answer" in labels
    assert "Reset" in labels


def test_submit_without_answer_shows_no_feedback_banner() -> None:
    """Check that submitting without input shows no result banner."""
    at = AppTest.from_function(render_molecule_question)

    with patch(
        "questions.MoleculeDrawingQuestion.jsme_component",
        return_value=None,
    ):
        at.run()
        get_button_by_label(at, "Submit Answer").click().run()

    text = all_text_content(at)

    assert "Your answer is correct!" not in text
    assert "Your answer is incorrect!" not in text


def test_submit_correct_answer_shows_success() -> None:
    """Check that submitting the correct molecule shows success."""
    at = AppTest.from_function(render_molecule_question)

    with patch(
        "questions.MoleculeDrawingQuestion.jsme_component",
        return_value={"smiles": "CCO"},
    ):
        at.run()
        get_button_by_label(at, "Submit Answer").click().run()

    text = all_text_content(at)

    assert "Your answer is correct!" in text
    assert "Your answer is incorrect!" not in text


def test_submit_incorrect_answer_shows_error() -> None:
    """Check that submitting an incorrect molecule shows error."""
    at = AppTest.from_function(render_molecule_question)

    with patch(
        "questions.MoleculeDrawingQuestion.jsme_component",
        return_value={"smiles": "CCC"},
    ):
        at.run()
        get_button_by_label(at, "Submit Answer").click().run()

    text = all_text_content(at)

    assert "Your answer is incorrect!" in text
    assert "Your answer is correct!" not in text


def test_session_state_only_does_not_count_as_component_answer() -> None:
    """Check that session state alone is not treated as drawn input."""
    at = AppTest.from_function(render_molecule_question)
    at.session_state[WIDGET_KEY] = "CCO"

    with patch(
        "questions.MoleculeDrawingQuestion.jsme_component",
        return_value=None,
    ):
        at.run()
        get_button_by_label(at, "Submit Answer").click().run()

    text = all_text_content(at)

    assert "Your answer is correct!" not in text
    assert "Your answer is incorrect!" not in text
