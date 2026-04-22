from unittest.mock import mock_open, patch

import numpy as np
import pytest
from plotly import graph_objects as go

from questions.SpectralQuestion import SpectralQuestion, SpectralType


def test_ir_figure_draws_selected_peak_line() -> None:
    """IR spectra should show a vertical guide line for the selected peak."""
    question = SpectralQuestion(
        "ir_question",
        "IR Question",
        "Select the peak",
        ["data/images/test.png"],
        "data/spectra/ir_sample.jdx",
        1700,
        ["Correct", "Incorrect"],
    )
    question.x = np.array([1600.0, 1700.0, 1800.0])
    question.y = np.array([90.0, 35.0, 80.0])
    question.units = "cm^-1"

    fig = question.build_figure(1700.0)

    assert len(fig.layout.shapes) == 1
    shape = fig.layout.shapes[0]
    assert shape["type"] == "line"
    assert shape["x0"] == 1700.0
    assert shape["x1"] == 1700.0


def test_non_ir_figure_does_not_draw_selected_peak_line() -> None:
    """Only IR spectra should get the selection guide line."""
    question = SpectralQuestion(
        "ms_question",
        "MS Question",
        "Select the peak",
        [""],
        "data/spectra/ms_sample.jdx",
        43,
        ["Correct", "Incorrect"],
    )
    question.type = SpectralType.MS
    question.x = np.array([20.0, 43.0, 70.0])
    question.y = np.array([10.0, 100.0, 30.0])
    question.units = "m/z"

    fig = question.build_figure(43.0)

    assert len(fig.layout.shapes) == 0


def test_detect_type_ms() -> None:
    """test to detect ms type."""
    question = SpectralQuestion(
        "ms_question",
        "MS Question",
        "Select the peak",
        "data/spectra/ms_sample.jdx",
        43,
        ["Correct", "Incorrect"],
    )
    assert question.type == SpectralType.MS


def test_detect_type_ir() -> None:
    """Test to detect ir type."""
    question = SpectralQuestion(
        "ir_question",
        "IR Question",
        "Select the peak",
        "data/spectra/ir_sample.jdx",
        1700,
        ["Correct", "Incorrect"],
    )
    assert question.type == SpectralType.IR


def test_detect_type_nmr() -> None:
    """Test to detect nmr type."""
    question = SpectralQuestion(
        "nmr_question",
        "NMR Question",
        "Select the peak",
        "data/spectra/nmr_sample.jdx",
        7.2,
        ["Correct", "Incorrect"],
    )
    assert question.type == SpectralType.NMR


def test_detect_type_invalid_file_raises_value_error() -> None:
    """Test that an invalid spectral file raises a ValueError."""
    with pytest.raises(ValueError):
        SpectralQuestion(
            "bad_question",
            "Bad Question",
            "Select the peak",
            "data/spectra/unknown_sample.jdx",
            10,
            ["Correct", "Incorrect"],
        )


def test_verify_and_feedback_correct_within_tolerance() -> None:
    """Test that a nearby correct value is accepted within tolerance."""
    question = SpectralQuestion(
        "ir_question",
        "IR Question",
        "Select the peak",
        "data/spectra/ir_sample.jdx",
        1700,
        ["Correct", "Incorrect"],
        tolerance=0.5,
    )

    assert question.verifyAndFeedback(1700.4) == (True, "Correct")


def test_verify_and_feedback_incorrect_outside_tolerance() -> None:
    """Test that a value outside tolerance is marked incorrect."""
    question = SpectralQuestion(
        "ir_question",
        "IR Question",
        "Select the peak",
        "data/spectra/ir_sample.jdx",
        1700,
        ["Correct", "Incorrect"],
        tolerance=0.5,
    )

    assert question.verifyAndFeedback(1701.0) == (False, "Incorrect")


def test_feedback_correct() -> None:
    """Test that feedback returns the correct message for a right answer."""
    question = SpectralQuestion(
        "ms_question",
        "MS Question",
        "Select the peak",
        "data/spectra/ms_sample.jdx",
        43,
        ["Correct", "Incorrect"],
        tolerance=1.0,
    )

    assert question.feedback(43) == "Correct"


def test_feedback_incorrect() -> None:
    """Test that feedback returns the incorrect message for a wrong answer."""
    question = SpectralQuestion(
        "ms_question",
        "MS Question",
        "Select the peak",
        "data/spectra/ms_sample.jdx",
        43,
        ["Correct", "Incorrect"],
        tolerance=0.5,
    )

    assert question.feedback(50) == "Incorrect"


def test_build_figure_ms_uses_bar_trace() -> None:
    """Test that MS spectra are drawn with a bar trace."""
    question = SpectralQuestion(
        "ms_question",
        "MS Question",
        "Select the peak",
        "data/spectra/ms_sample.jdx",
        43,
        ["Correct", "Incorrect"],
    )
    question.x = np.array([20.0, 43.0, 70.0])
    question.y = np.array([10.0, 100.0, 30.0])
    question.units = "m/z"

    fig = question.build_figure()

    assert len(fig.data) == 1
    assert isinstance(fig.data[0], go.Bar)


def test_build_figure_ir_uses_line_trace() -> None:
    """Test that IR spectra are drawn with a line trace."""
    question = SpectralQuestion(
        "ir_question",
        "IR Question",
        "Select the peak",
        "data/spectra/ir_sample.jdx",
        1700,
        ["Correct", "Incorrect"],
    )
    question.x = np.array([1600.0, 1700.0, 1800.0])
    question.y = np.array([90.0, 35.0, 80.0])
    question.units = "cm^-1"

    fig = question.build_figure()

    assert len(fig.data) == 1
    assert fig.data[0].type == "scatter"


def test_build_figure_sets_layout_titles() -> None:
    """Test that the figure layout titles are set correctly."""
    question = SpectralQuestion(
        "ir_question",
        "IR Question",
        "Select the peak",
        "data/spectra/ir_sample.jdx",
        1700,
        ["Correct", "Incorrect"],
    )
    question.x = np.array([1600.0, 1700.0, 1800.0])
    question.y = np.array([90.0, 35.0, 80.0])
    question.units = "cm^-1"

    fig = question.build_figure()

    assert fig.layout.title.text == "IR Question"
    assert fig.layout.xaxis.title.text == "cm^-1"
    assert fig.layout.yaxis.title.text == "Transmittance"


def test_parse_jcampdx_sets_x_y_and_units() -> None:
    """Test that JCAMP-DX parsing sets x, y, and units correctly."""
    question = SpectralQuestion(
        "ms_question",
        "MS Question",
        "Select the peak",
        "data/spectra/ms_sample.jdx",
        43,
        ["Correct", "Incorrect"],
    )

    fake_bytes = b"##TITLE=Example\n##END="

    with patch("builtins.open", mock_open(read_data=fake_bytes)):
        with patch("jcamp.jcamp_read") as mock_read:
            mock_read.return_value = {
                "x": [10, 20, 30],
                "y": [1, 2, 4],
                "xunits": "m/z",
            }

            question._parse_jcampdx()  # noqa: SLF001

    assert np.array_equal(question.x, np.array([10.0, 20.0, 30.0]))
    assert np.array_equal(question.y, np.array([25.0, 50.0, 100.0]))
    assert question.units == "m/z"


def test_parse_jcampdx_returns_early_when_imgpath_is_none() -> None:
    """Test that parsing returns early when no image path is provided."""
    question = SpectralQuestion.__new__(SpectralQuestion)
    question.imgpath = None

    result = question._parse_jcampdx()  # noqa: SLF001

    assert result is None
