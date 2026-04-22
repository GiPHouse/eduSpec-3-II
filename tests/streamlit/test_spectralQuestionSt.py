from streamlit.testing.v1 import AppTest


def render_spectral_question() -> None:
    """Render a spectral question in a Streamlit test app."""
    from questions.SpectralQuestion import SpectralQuestion

    question = SpectralQuestion(
        "ir_question",
        "IR Question",
        "Select the peak",
        "data/spectra/ir_sample.jdx",
        1700,
        ["Correct", "Incorrect"],
    )
    question.drawYourself()


def all_text_content(at: AppTest) -> str:
    """Collect all visible text content from the app."""
    parts: list[str] = []

    for node_list_name in (
        "markdown",
        "text",
        "caption",
        "latex",
        "exception",
        "warning",
        "info",
        "success",
        "error",
    ):
        if hasattr(at, node_list_name):
            for node in getattr(at, node_list_name):
                if hasattr(node, "value") and node.value is not None:
                    parts.append(str(node.value))

    return " ".join(parts)


def test_spectral_draw_yourself_shows_info_when_no_peak_selected() -> None:
    """Test that spectral question shows info when no peak is selected."""
    at = AppTest.from_function(render_spectral_question)
    at.run()

    assert not at.exception
    text = all_text_content(at)
    assert "Click a peak on the spectrum to select it." in text


def test_spectral_draw_yourself_shows_selected_peak_when_present() -> None:
    """Test that spectral question shows the selected peak from session state."""
    at = AppTest.from_function(render_spectral_question)
    at.session_state["spectral_question_ir_question"] = 1700.0
    at.run()

    assert not at.exception
    text = all_text_content(at)
    assert "Selected peak: 1700.0 cm^-1" in text
