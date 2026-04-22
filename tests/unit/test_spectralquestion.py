from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

import numpy as np
import pytest

from questions.SpectralQuestion import SpectralQuestion, SpectralType


def make_question(path: str = "data/spectra/ir_sample.jdx") -> SpectralQuestion:
    """Create a spectral question for testing."""
    return SpectralQuestion(
        "spec_q1",
        "IR Question",
        "Select the peak",
        None,
        path,
        1700.0,
        ["Correct", "Incorrect"],
        tolerance=0.5,
    )


def test_detect_type_ms_returns_ms() -> None:
    """Detect MS spectra from the path."""
    question = make_question("data/spectra/ms_sample.jdx")
    assert question.type == SpectralType.MS


def test_detect_type_ir_returns_ir() -> None:
    """Detect IR spectra from the path."""
    question = make_question("data/spectra/ir_sample.jdx")
    assert question.type == SpectralType.IR


def test_detect_type_nmr_returns_nmr() -> None:
    """Detect NMR spectra from the path."""
    question = make_question("data/spectra/nmr_sample.jdx")
    assert question.type == SpectralType.NMR


def test_detect_type_invalid_file_raises_value_error() -> None:
    """Raise ValueError for unsupported spectral paths."""
    with pytest.raises(ValueError):
        make_question("data/spectra/unknown_sample.jdx")


def test_verify_and_feedback_correct_within_tolerance() -> None:
    """Mark answers within tolerance as correct."""
    question = make_question()
    assert question.verifyAndFeedback(1700.4) == (True, "Correct")


def test_verify_and_feedback_incorrect_outside_tolerance() -> None:
    """Mark answers outside tolerance as incorrect."""
    question = make_question()
    assert question.verifyAndFeedback(1701.0) == (False, "Incorrect")


def test_feedback_returns_correct_message() -> None:
    """Return positive feedback for correct answers."""
    question = make_question()
    assert question.feedback(1700.0) == "Correct"


def test_feedback_returns_incorrect_message() -> None:
    """Return negative feedback for incorrect answers."""
    question = make_question()
    assert question.feedback(1690.0) == "Incorrect"


def test_parse_jcampdx_sets_x_y_and_units(tmp_path: Any) -> None:
    """Parse JCAMP data and store normalized arrays and units."""
    spectral_file = tmp_path / "ir_sample.jdx"
    spectral_file.write_bytes(b"##TITLE=Fake\n##END=")

    question = make_question(str(spectral_file))

    fake_data = {
        "x": [1000.0, 1500.0, 2000.0],
        "y": [1.0, 2.0, 4.0],
        "xunits": "cm^-1",
    }

    with patch("questions.SpectralQuestion.jcamp.jcamp_read", return_value=fake_data):
        question._parse_jcampdx()  # noqa : SLF001

    assert np.allclose(question.x, np.asarray([1000.0, 1500.0, 2000.0], dtype=float))
    assert np.allclose(question.y, np.asarray([25.0, 50.0, 100.0], dtype=float))
    assert question.units == "cm^-1"


def test_parse_jcampdx_uses_default_unit_when_missing(tmp_path: Any) -> None:
    """Use m/z when xunits are missing."""
    spectral_file = tmp_path / "ms_sample.jdx"
    spectral_file.write_bytes(b"##TITLE=Fake\n##END=")

    question = make_question(str(spectral_file))

    fake_data = {
        "x": [10.0, 20.0],
        "y": [1.0, 2.0],
    }

    with patch("questions.SpectralQuestion.jcamp.jcamp_read", return_value=fake_data):
        question._parse_jcampdx()  # noqa : SLF001

    assert question.units == "m/z"


def test_build_figure_for_ms_adds_bar_trace() -> None:
    """Build a bar chart for MS spectra."""
    question = make_question("data/spectra/ms_sample.jdx")
    question.x = np.asarray([10.0, 20.0, 30.0], dtype=float)
    question.y = np.asarray([30.0, 60.0, 90.0], dtype=float)
    question.units = "m/z"

    figure = question.build_figure()

    assert len(figure.data) == 1
    assert figure.data[0].type == "bar"
    assert figure.layout.xaxis.title.text == "m/z"
    assert figure.layout.yaxis.title.text == question.type.y_label


def test_build_figure_for_ir_adds_scatter_trace() -> None:
    """Build a line chart for non-MS spectra."""
    question = make_question("data/spectra/ir_sample.jdx")
    question.x = np.asarray([1000.0, 1500.0, 2000.0], dtype=float)
    question.y = np.asarray([10.0, 50.0, 90.0], dtype=float)
    question.units = "cm^-1"

    figure = question.build_figure()

    assert len(figure.data) == 1
    assert figure.data[0].type == "scatter"
    assert figure.layout.xaxis.title.text == "cm^-1"
    assert figure.layout.yaxis.title.text == question.type.y_label


def test_build_figure_for_ir_with_selected_x_adds_vline() -> None:
    """Add a vertical marker for selected IR peaks."""
    question = make_question("data/spectra/ir_sample.jdx")
    question.x = np.asarray([1000.0, 1500.0, 2000.0], dtype=float)
    question.y = np.asarray([10.0, 50.0, 90.0], dtype=float)
    question.units = "cm^-1"

    figure = question.build_figure(selected_x=1500.0)

    assert len(figure.layout.shapes) == 1
    assert figure.layout.shapes[0].type == "line"
    assert figure.layout.shapes[0].x0 == 1500.0
    assert figure.layout.shapes[0].x1 == 1500.0


def test_draw_yourself_returns_selected_value() -> None:
    """Return the selected value from session state."""
    question = make_question()

    with (
        patch("questions.SpectralQuestion.st.session_state", {question.widget_key: 1700.0}),
        patch.object(question, "drawSpectralGraph"),
        patch("questions.SpectralQuestion.st.write") as mock_write,
        patch("questions.SpectralQuestion.st.info") as mock_info,
    ):
        selected = question.drawYourself()

    assert selected == 1700.0
    mock_write.assert_called_once_with("Selected peak: 1700.0 cm^-1")
    mock_info.assert_not_called()


def test_draw_yourself_shows_info_when_no_selection() -> None:
    """Show an info message when no peak is selected."""
    question = make_question()

    with (
        patch("questions.SpectralQuestion.st.session_state", {}),
        patch.object(question, "drawSpectralGraph"),
        patch("questions.SpectralQuestion.st.write") as mock_write,
        patch("questions.SpectralQuestion.st.info") as mock_info,
    ):
        selected = question.drawYourself()

    assert selected is None
    mock_write.assert_not_called()
    mock_info.assert_called_once_with("Click a peak on the spectrum to select it.")


def test_draw_spectral_graph_updates_selection_and_reruns() -> None:
    """Store clicked peak x value and rerun the app."""
    question = make_question()
    question.x = np.asarray([1000.0, 1500.0, 2000.0], dtype=float)
    question.y = np.asarray([10.0, 50.0, 90.0], dtype=float)
    question.units = "cm^-1"

    fake_state: dict[str, Any] = {}
    event = SimpleNamespace(selection=SimpleNamespace(points=[{"point_index": 1}]))

    with (
        patch("questions.SpectralQuestion.st.session_state", fake_state),
        patch.object(question, "_parse_jcampdx"),
        patch.object(question, "build_figure", return_value="fake_fig"),
        patch("questions.SpectralQuestion.st.plotly_chart", return_value=event),
        patch("questions.SpectralQuestion.st.rerun") as mock_rerun,
    ):
        question.drawSpectralGraph()

    assert fake_state[question.widget_key] == 1500.0
    mock_rerun.assert_called_once()


def test_draw_spectral_graph_does_not_rerun_when_same_selection() -> None:
    """Avoid rerunning when the same peak is selected again."""
    question = make_question()
    question.x = np.asarray([1000.0, 1500.0, 2000.0], dtype=float)
    question.y = np.asarray([10.0, 50.0, 90.0], dtype=float)
    question.units = "cm^-1"

    fake_state: dict[str, Any] = {question.widget_key: 1500.0}
    event = SimpleNamespace(selection=SimpleNamespace(points=[{"point_index": 1}]))

    with (
        patch("questions.SpectralQuestion.st.session_state", fake_state),
        patch.object(question, "_parse_jcampdx"),
        patch.object(question, "build_figure", return_value="fake_fig"),
        patch("questions.SpectralQuestion.st.plotly_chart", return_value=event),
        patch("questions.SpectralQuestion.st.rerun") as mock_rerun,
    ):
        question.drawSpectralGraph()

    assert fake_state[question.widget_key] == 1500.0
    mock_rerun.assert_not_called()
