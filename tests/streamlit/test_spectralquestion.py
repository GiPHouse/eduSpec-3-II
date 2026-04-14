from streamlit.testing.v1 import AppTest

from QuestionDrawer import QuestionDrawer
from questions.SpectralQuestion import SpectralQuestion
from tests.streamlit.helpers import all_text_content, get_button_by_label


def make_question() -> SpectralQuestion:
    return SpectralQuestion(
        name="spec1",
        title="IR Peak",
        bodytext="Select the carbonyl peak in the spectrum.",
        imgpath="data/spectra/ir.dx",
        correct_answer=1700.0,
        feedbacks=["Peak identified.", "That is not the target peak."],
        tolerance=50.0,
    )


def render_spectral_question() -> None:
    QuestionDrawer.drawQuestion(make_question())


def test_spectral_question_renders_chart_and_download_button() -> None:
    at = AppTest.from_function(render_spectral_question)
    at.run()

    assert at.title[0].value == "IR Peak"
    assert "Select the carbonyl peak in the spectrum." in all_text_content(at)
    assert len(at.plotly_chart) == 1
    assert any(button.label == "Download Spectral Data" for button in at.button)


def test_spectral_question_initial_prompt_is_visible_without_selection() -> None:
    at = AppTest.from_function(render_spectral_question)
    at.run()

    assert "Click a peak on the spectrum to select it." in all_text_content(at)


def test_spectral_question_submit_selected_peak_shows_success() -> None:
    at = AppTest.from_function(render_spectral_question)
    at.session_state["spectral_question_spec1"] = 1700.0
    at.run()

    get_button_by_label(at, "Submit Answer").click().run()

    assert "Selected peak: 1700.0 cm^-1" in all_text_content(at)
    assert "Your answer is correct!" in all_text_content(at)
    assert "Peak identified." in all_text_content(at)


def test_spectral_question_reset_clears_selected_peak() -> None:
    at = AppTest.from_function(render_spectral_question)
    at.session_state["spectral_question_spec1"] = 1700.0
    at.run()

    get_button_by_label(at, "Reset").click().run()

    assert at.session_state["spectral_question_spec1"] is None
