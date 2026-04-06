from streamlit.testing.v1 import AppTest

from QuestionDrawer import QuestionDrawer
from questions.MoleculeDrawingQuestion import (
    MoleculeDrawingConfig,
    MoleculeDrawingQuestion,
)

EXPECTED = "CCO"
WIDGET_KEY = "q1"


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
    )

    QuestionDrawer.drawQuestion(q)


def get_button_by_label(at: AppTest, label: str) -> object:
    """Return the first button whose label matches the given text."""
    return next(b for b in at.button if b.label == label)


def all_text_content(at: AppTest) -> str:
    """Collect visible text-like content from the rendered app."""
    parts = []
    parts.extend(x.value for x in at.title)
    parts.extend(x.value for x in at.text)
    parts.extend(x.value for x in at.markdown)
    parts.extend(x.value for x in at.info)
    return " ".join(str(x) for x in parts)


# Python logic tests


def test_verify_correct_smiles() -> None:
    """Check that the correct SMILES string is accepted."""
    q = make_question()
    ok, msg = q.verifyAndFeedback("CCO")
    assert ok is True
    assert "Correct" in msg or "correct" in msg
    assert "Incorrect" not in msg
    assert "incorrect" not in msg


def test_verify_incorrect_smiles_contains_expected_and_actual() -> None:
    """Check that an incorrect SMILES string is rejected."""
    q = make_question()
    ok, msg = q.verifyAndFeedback("CCC")
    assert ok is False
    assert "Inorrect" in msg or "incorrect" in msg


def test_verify_empty_smiles_returns_error() -> None:
    """Check that an empty SMILES string returns an error message."""
    q = make_question()
    ok, msg = q.verifyAndFeedback("")
    assert ok is False
    assert "No SMILES found" in msg


def test_feedback_message_default() -> None:
    """Check that the default feedback message is returned."""
    q = make_question()
    msg = q.feedback()
    assert isinstance(msg, str)
    assert "Try again" in msg


def test_constructor_sets_basic_fields() -> None:
    """Check that constructor values are stored correctly."""
    q = make_question(seed_smiles="C")
    assert q.widget_key == WIDGET_KEY
    assert q.default == "C"
    assert q.correct_answer == EXPECTED


# App rendering tests


def test_page_renders_title_and_prompt() -> None:
    """Check that the page shows the expected title and prompt."""
    at = AppTest.from_function(render_molecule_question)
    at.run()

    assert len(at.title) == 1
    assert at.title[0].value == "Draw ethanol"
    assert "Use the editor to draw ethanol and submit." in all_text_content(at)


def test_submit_and_reset_buttons_render() -> None:
    """Check that submit and reset buttons are rendered."""
    at = AppTest.from_function(render_molecule_question)
    at.run()

    labels = [b.label for b in at.button]
    assert "Submit Answer" in labels
    assert "Reset" in labels


def test_info_message_is_shown_initially() -> None:
    """Check that the initial info message is shown."""
    at = AppTest.from_function(render_molecule_question)
    at.run()

    text = all_text_content(at)
    assert "Draw a molecule in the editor" in text


def test_app_has_no_exception_on_first_run() -> None:
    """Check that the app renders without exceptions on first run."""
    at = AppTest.from_function(render_molecule_question)
    at.run()

    assert len(at.exception) == 0


# Submit flow tests


def test_submit_without_answer_shows_no_correct_or_incorrect_banner() -> None:
    """Check that submitting without input shows no result banner."""
    at = AppTest.from_function(render_molecule_question)
    at.run()

    submit_button = get_button_by_label(at, "Submit Answer")
    submit_button.click().run()

    text = all_text_content(at)
    assert "Your answer is correct!" not in text
    assert "Your answer is incorrect!" not in text


def test_submit_with_session_state_only_does_not_trigger_evaluation() -> None:
    """Check that session state alone does not trigger evaluation."""
    at = AppTest.from_function(render_molecule_question)
    at.session_state[WIDGET_KEY] = "CCO"
    at.run()

    submit_button = get_button_by_label(at, "Submit Answer")
    submit_button.click().run()

    text = all_text_content(at)
    assert "Your answer is correct!" not in text
    assert "Your answer is incorrect!" not in text


def test_submit_correct_answer_does_not_show_failure() -> None:
    """Check that a correct answer does not show failure feedback."""
    at = AppTest.from_function(render_molecule_question)
    at.session_state[WIDGET_KEY] = "CCO"
    at.run()

    submit_button = get_button_by_label(at, "Submit Answer")
    submit_button.click().run()

    text = all_text_content(at)
    assert "Your answer is incorrect!" not in text


def test_submit_incorrect_answer_does_not_show_success() -> None:
    """Check that an incorrect answer does not show success feedback."""
    at = AppTest.from_function(render_molecule_question)
    at.session_state[WIDGET_KEY] = "CCC"
    at.run()

    submit_button = get_button_by_label(at, "Submit Answer")
    submit_button.click().run()

    text = all_text_content(at)
    assert "Your answer is correct!" not in text


# Reset flow tests


def test_reset_clears_widget_state() -> None:
    """Check that reset clears the widget state."""
    at = AppTest.from_function(render_molecule_question)
    at.session_state[WIDGET_KEY] = "CCO"
    at.run()

    reset_button = get_button_by_label(at, "Reset")
    reset_button.click().run()

    assert at.session_state[WIDGET_KEY] == ""


def test_reset_after_incorrect_value_clears_state() -> None:
    """Check that reset clears state after an incorrect value."""
    at = AppTest.from_function(render_molecule_question)
    at.session_state[WIDGET_KEY] = "CCC"
    at.run()

    reset_button = get_button_by_label(at, "Reset")
    reset_button.click().run()

    assert at.session_state[WIDGET_KEY] == ""


# Session state / internal key tests


def test_internal_nonce_key_created() -> None:
    """Check that the internal nonce key is created."""
    at = AppTest.from_function(render_molecule_question)
    at.run()

    assert f"{WIDGET_KEY}__jsme_nonce" in at.session_state


def test_internal_last_seen_key_created() -> None:
    """Check that the internal last-seen key is created."""
    at = AppTest.from_function(render_molecule_question)
    at.run()

    assert f"{WIDGET_KEY}__last_seen" in at.session_state


def test_widget_key_exists_after_first_run() -> None:
    """Check that the widget key exists after the first run."""
    at = AppTest.from_function(render_molecule_question)
    at.run()

    assert WIDGET_KEY in at.session_state


# Edge case


def test_whitespace_only_input_is_treated_as_empty_in_direct_logic() -> None:
    """Check that whitespace-only input is treated as empty."""
    q = make_question()
    ok, msg = q.verifyAndFeedback("   ")
    assert ok is False
    assert "No SMILES found" in msg
