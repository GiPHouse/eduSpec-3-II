"""Tests for SpectralQuestion.

Replace the spectralpath value inside render_spectral_question() with a real
.jdx / .dx file from your repo. Every value used inside that function must be
a literal — AppTest.from_function copies source code into a temp script where
no module-level names exist.
"""

from streamlit.testing.v1 import AppTest

WIDGET_KEY = "spectral_question_sq1"
CORRECT_ANSWER = 100.0
TOLERANCE = 0.5


# ── AppTest render function ───────────────────────────────────────────────────
# IMPORTANT: AppTest.from_function serialises this function's *source code*
# and runs it in a fresh interpreter with no surrounding scope.
# Every value must therefore be a hard-coded literal inside this function.


def render_spectral_question() -> None:
    """_summary_"""
    from QuestionDrawer import QuestionDrawer
    from questions.SpectralQuestion import SpectralQuestion

    question = SpectralQuestion(
        name="sq1",
        title="Spectral Question",
        bodytext="Click the correct peak.",
        figures=None,
        spectralpath="ms.dx",  # <-- replace with your path
        correct_answer=100.0,
        feedbacks=["Correct!", "Incorrect!"],
        tolerance=0.5,
    )
    QuestionDrawer.drawQuestion(question)


# ── helper for pure-logic tests (does NOT use AppTest) ────────────────────────

# ── rendering ─────────────────────────────────────────────────────────────────


class TestSpectralQuestionRendering:
    """_summary_"""

    def test_renders_without_exception(self) -> None:
        """_summary_"""
        at = AppTest.from_function(render_spectral_question)
        at.run()
        assert not at.exception

    def test_title_is_displayed(self) -> None:
        """_summary_"""
        at = AppTest.from_function(render_spectral_question)
        at.run()
        assert not at.exception
        assert any(t.value == "Spectral Question" for t in at.title)

    def test_body_text_is_displayed(self) -> None:
        """_summary_"""
        at = AppTest.from_function(render_spectral_question)
        at.run()
        assert not at.exception
        assert any("Click the correct peak." in t.value for t in at.text)

    def test_default_state_shows_info_message(self) -> None:
        """_summary_"""
        at = AppTest.from_function(render_spectral_question)
        at.run()
        assert not at.exception
        assert any("Click a peak" in i.value for i in at.info)

    def test_submit_and_reset_buttons_exist(self) -> None:
        """_summary_"""
        at = AppTest.from_function(render_spectral_question)
        at.run()
        assert not at.exception
        labels = [b.label for b in at.button]
        assert any("Submit" in label for label in labels)
        assert any("Reset" in label for label in labels)


# ── session state injection ───────────────────────────────────────────────────
# Plotly click events are frontend-only; AppTest cannot fire them.
# We simulate them by writing directly to session_state before re-running.


class TestSpectralQuestionSessionState:
    """_summary_"""

    def test_selected_peak_removes_info_message(self) -> None:
        """_summary_"""
        at = AppTest.from_function(render_spectral_question)
        at.run()
        assert not at.exception

        at.session_state[WIDGET_KEY] = CORRECT_ANSWER
        at.run()
        assert not at.exception
        assert not any("Click a peak" in i.value for i in at.info)

    def test_selected_peak_value_is_shown(self) -> None:
        """_summary_"""
        at = AppTest.from_function(render_spectral_question)
        at.run()
        assert not at.exception

        at.session_state[WIDGET_KEY] = CORRECT_ANSWER
        at.run()
        assert not at.exception

        # drawYourself writes e.g. "Selected peak: **100.000 m/z**"
        all_markdown = " ".join(e.value for e in at.markdown)
        assert f"{CORRECT_ANSWER:.3f}" in all_markdown

    def test_reset_clears_selection(self) -> None:
        """_summary_"""
        """Test that reset clears the info about previously selected peak"""
        at = AppTest.from_function(render_spectral_question)
        at.run()
        assert not at.exception

        at.session_state[WIDGET_KEY] = CORRECT_ANSWER
        at.run()
        assert not at.exception

        at.button(key="reset_button_form_sq1").click().run()
        assert not at.exception
        assert at.session_state[WIDGET_KEY] is None


# ── submit / evaluate ─────────────────────────────────────────────────────────


class TestSpectralQuestionSubmit:
    """_summary_"""

    def test_correct_answer_shows_success(self) -> None:
        """_summary_"""
        at = AppTest.from_function(render_spectral_question)
        at.run()
        assert not at.exception

        at.session_state[WIDGET_KEY] = CORRECT_ANSWER
        at.run()
        assert not at.exception

        at.button(key="submit_button_form_sq1").click().run()
        assert not at.exception
        assert any("correct" in s.value.lower() for s in at.success)

    def test_wrong_answer_shows_error(self) -> None:
        """_summary_"""
        at = AppTest.from_function(render_spectral_question)
        at.run()
        assert not at.exception

        at.session_state[WIDGET_KEY] = CORRECT_ANSWER + TOLERANCE + 1.0
        at.run()
        assert not at.exception

        at.button(key="submit_button_form_sq1").click().run()
        assert not at.exception
        assert any("incorrect" in e.value.lower() for e in at.error)

    def test_no_feedback_without_selection(self) -> None:
        """_summary_"""
        at = AppTest.from_function(render_spectral_question)
        at.run()
        assert not at.exception

        at.button(key="submit_button_form_sq1").click().run()
        assert not at.exception
        assert len(at.success) == 0
        assert len(at.error) == 0


# ── pure logic (no AppTest) ───────────────────────────────────────────────────
