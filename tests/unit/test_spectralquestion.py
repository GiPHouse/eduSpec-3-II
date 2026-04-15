import numpy as np

from questions.SpectralQuestion import SpectralQuestion, SpectralType


def test_ir_figure_draws_selected_peak_line() -> None:
    """IR spectra should show a vertical guide line for the selected peak."""
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
