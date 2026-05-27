import pytest

from questions.SpectralQuestion import SpectralQuestion

"""Tests for SpectralQuestion.

Replace the spectralpath value inside render_spectral_question() with a real
.jdx / .dx file from your repo. Every value used inside that function must be
a literal — AppTest.from_function copies source code into a temp script where
no module-level names exist.
"""

"""
FOR THIS UNIT TEST TO WORK, IT MUST BE IN THIS DIRECTORY, BECAUSE OF THE HANDLING OF SPECTRAL DATA

"""


WIDGET_KEY = "spectral_question_sq1"
CORRECT_ANSWER = 100.0
TOLERANCE = 0.5


# ── AppTest render function ───────────────────────────────────────────────────
# IMPORTANT: AppTest.from_function serialises this function's *source code*
# and runs it in a fresh interpreter with no surrounding scope.
# Every value must therefore be a hard-coded literal inside this function.

# ── helper for pure-logic tests (does NOT use AppTest) ────────────────────────


def make_question() -> SpectralQuestion:
    """_summary_

    Returns:
        SpectralQuestion: _description_
    """
    return SpectralQuestion(
        name="sq1",
        title="Spectral Question",
        bodytext="Click the correct peak.",
        figures=None,
        spectralpath="ms.dx",  # <-- replace with your path
        correct_answer=CORRECT_ANSWER,
        feedbacks=["Correct!", "Incorrect!"],
        tolerance=TOLERANCE,
    )


# ── rendering ─────────────────────────────────────────────────────────────────


# ── session state injection ───────────────────────────────────────────────────
# Plotly click events are frontend-only; AppTest cannot fire them.
# We simulate them by writing directly to session_state before re-running.

# ── pure logic (no AppTest) ───────────────────────────────────────────────────


class TestVerifyAndFeedback:
    """_summary_"""

    def test_correct_within_tolerance(self) -> None:
        """_summary_"""
        q = make_question()
        is_correct, msg = q.verifyAndFeedback(CORRECT_ANSWER)
        assert is_correct
        assert msg == "Correct!"

    def test_correct_at_tolerance_boundary(self) -> None:
        """_summary_"""
        q = make_question()
        is_correct, _ = q.verifyAndFeedback(CORRECT_ANSWER + TOLERANCE)
        assert is_correct

    def test_wrong_just_outside_tolerance(self) -> None:
        """_summary_"""
        q = make_question()
        is_correct, msg = q.verifyAndFeedback(CORRECT_ANSWER + TOLERANCE + 0.01)
        assert not is_correct
        assert msg == "Incorrect!"

    def test_none_raises_type_error(self) -> None:
        """_summary_"""
        q = make_question()
        with pytest.raises(TypeError):
            q.verifyAndFeedback(None)

    def test_feedback_correct(self) -> None:
        """_summary_"""
        q = make_question()
        assert q.feedback(CORRECT_ANSWER) == "Correct!"

    def test_feedback_incorrect(self) -> None:
        """_summary_"""
        q = make_question()
        assert q.feedback(CORRECT_ANSWER + 999) == "Incorrect!"
