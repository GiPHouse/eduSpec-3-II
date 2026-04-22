# questions/SpectralQuestion.py

import re
from enum import Enum
from typing import List, Optional, Tuple

import jcamp
import numpy as np
import streamlit as st
from plotly import graph_objects as go

from questions.NMRParser import loadJCAMP
from questions.Question import Question


@st.cache_data
def load_nmr(imgpath: str) -> None:
    """Just a function to wrap external loadJCAMP with st.cache_data

    Args:
        imgpath (str): the path to the spectral data

    Returns:
        None: None
    """
    return loadJCAMP(imgpath)


@st.cache_data
def load_non_nmr_jcamp(imgpath: str) -> Tuple[np.ndarray, np.ndarray, str]:
    """A function to load non_nmr data.

    Args:
        imgpath (str): Path to the spectral data

    Returns:
        Tuple[np.ndarray, np.ndarray, str]: The x and y axes of the data alongiside the unit as a string
    """
    with open(imgpath, "rb") as f:
        lines = [ln.decode("utf-8", errors="replace") for ln in f.read().splitlines()]

    data = jcamp.jcamp_read(lines)
    x = np.asarray(data["x"], dtype=float)
    y = np.asarray(data["y"], dtype=float)

    if y.size > 0 and np.max(y) > 0:
        y = (y / np.max(y)) * 100.0

    units = data.get("xunits", "m/z")
    return x, y, units


class SpectralType(Enum):
    """Enum for each spectral type

    Args:
        Enum (_type_): Just Python way to create enums, its inheritance.
    """

    MS = ("MS", "m/z", "Intensity")
    IR = ("IR", "cm⁻¹", "Transmittance")
    NMR = ("NMR", "ppm", "Intensity")

    def __init__(self, label: str, unit: str, y_label: str):
        """Initialize the enum

        Args:
            label (str): Name of the spectral type
            unit (str): Units to measure it
            y_label (str): What the y-label is called.
        """
        self.label = label
        self.unit = unit
        self.y_label = y_label


class SpectralQuestion(Question):
    """A class to represent spectral questions

    Args:
        Question (): Inheritence

    Raises:
        ValueError: error
        ValueError: error
        ValueError: error

    Returns:
        _type_: nothing
    """

    NMR_MAX_DISPLAY_POINTS = 4000
    IR_MAX_DISPLAY_POINTS = 5000

    def __init__(
        self,
        name: str,
        title: str,
        bodytext: str,
        imgpath: Optional[list[str]],
        spectralpath: str,
        correct_answer: float,
        feedbacks: List[str],
        tolerance: float = 0.5,
    ):
        """Init for the class

        Args:
            name (str): Question id for JSON
            title (str): Question title
            bodytext (str): The question itself
            imgpath (Optional[str]): Path to the spectral question
            correct_answer (float): The correct answer
            feedbacks (List[str]): Feedbacks stored in the form of [correct,wrong]
            tolerance (float, optional): How much can user answer differ from actual correct answer. Defaults to 0.5.
        """
        super().__init__(name, title, bodytext, imgpath)

        self.correct_answer = correct_answer
        self.feedbacks = feedbacks
        self.tolerance = tolerance

        self.widget_key = f"spectral_question_{name}"
        self.chart_key = f"spectral_chart_{name}"
        self.default = None

        self.type = self._detect_type(imgpath)

        self.x: Optional[np.ndarray] = None
        self.y: Optional[np.ndarray] = None
        self.units: Optional[str] = None

        self.display_x: Optional[np.ndarray] = None
        self.display_y: Optional[np.ndarray] = None
        self.display_idx: Optional[np.ndarray] = None

        self._data_loaded = False

    def verifyAndFeedback(self, user_input: float) -> tuple[bool, str]:
        """Function to verify user answers

        Args:
            user_input (float): _description_

        Returns:
            tuple[bool, str]: _description_
        """
        is_correct = abs(user_input - self.correct_answer) <= self.tolerance
        return is_correct, self.feedback(user_input)

    def feedback(self, user_input: float) -> str:
        """The function to give feedback

        Args:
            user_input (float): _description_

        Returns:
            str: _description_
        """
        return (
            self.feedbacks[0]
            if abs(user_input - self.correct_answer) <= self.tolerance
            else self.feedbacks[1]
        )

    def _parse_jcampdx(self) -> None:
        if self._data_loaded:
            return

        if self.imgpath is None:
            raise ValueError("No spectral file provided")

        if self.type == SpectralType.NMR:
            x, y, isotope = load_nmr(self.imgpath)
            y = (y / np.max(y)) * 100 if np.max(y) > 0 else y
            self.units = f"δ {isotope} / ppm" if isotope else "δ / ppm"
            self.x, self.y = x, y
            self.display_x, self.display_y, self.display_idx = self._decimate_preserve_shape(
                x, y, self.NMR_MAX_DISPLAY_POINTS
            )
        else:
            x, y, units = load_non_nmr_jcamp(self.imgpath)
            self.x, self.y = x, y
            self.units = units

            if self.type == SpectralType.IR:
                self.display_x, self.display_y, self.display_idx = self._decimate_preserve_shape(
                    x, y, self.IR_MAX_DISPLAY_POINTS
                )
            else:
                self.display_x = x
                self.display_y = y
                self.display_idx = np.arange(len(x), dtype=int)

        self._data_loaded = True

    # questions/SpectralQuestion.py

    @staticmethod
    def _decimate_preserve_shape(
        x: np.ndarray,
        y: np.ndarray,
        max_points: int,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        n = len(x)
        full_idx = np.arange(n, dtype=int)

        if n <= max_points:
            return x, y, full_idx

        if max_points < 4:
            keep = np.array([0, int(np.argmax(y)), int(np.argmin(y)), n - 1], dtype=int)
            keep = np.unique(np.clip(keep, 0, n - 1))
            return x[keep], y[keep], keep

        bucket_count = max(1, max_points // 2)
        edges = np.linspace(0, n, bucket_count + 1, dtype=int)

        keep: list[int] = [0, n - 1, int(np.argmax(y)), int(np.argmin(y))]

        for start, end in zip(edges[:-1], edges[1:]):
            if end <= start:
                continue

            segment = y[start:end]
            local_max = start + int(np.argmax(segment))
            local_min = start + int(np.argmin(segment))

            keep.append(local_max)
            keep.append(local_min)

        keep = np.array(sorted(set(keep)), dtype=int)

        if len(keep) > max_points:
            chosen = np.linspace(0, len(keep) - 1, max_points, dtype=int)
            keep = keep[chosen]

            must_keep = np.array([0, n - 1, int(np.argmax(y)), int(np.argmin(y))], dtype=int)
            keep = np.array(sorted(set(keep).union(set(must_keep))), dtype=int)

            if len(keep) > max_points:
                protected = set(must_keep.tolist())
                optional = [idx for idx in keep if idx not in protected]

                remaining_slots = max_points - len(protected)
                if remaining_slots > 0 and optional:
                    chosen_optional = np.linspace(0, len(optional) - 1, remaining_slots, dtype=int)
                    keep = np.array(
                        sorted(list(protected) + [optional[i] for i in chosen_optional]), dtype=int
                    )
                else:
                    keep = np.array(sorted(protected), dtype=int)

        return x[keep], y[keep], keep

    def _snap_from_original_index(self, original_idx: int, window: int = 25) -> float:
        x = self.x
        y = self.y

        if x is None or y is None:
            raise ValueError("Spectral data not loaded")

        lo = max(0, original_idx - window)
        hi = min(len(x), original_idx + window + 1)

        seg_x = x[lo:hi]
        seg_y = y[lo:hi]

        if self.type == SpectralType.IR:
            local_idx = int(np.argmin(seg_y))
        elif self.type == SpectralType.NMR:
            local_idx = int(np.argmax(seg_y))
        else:
            local_idx = int(np.argmax(seg_y))

        return float(seg_x[local_idx])

    def drawImage(self) -> None:
        """A function to plot the spectral data and get user input"""
        self._parse_jcampdx()

        selected = st.session_state.get(self.widget_key, self.default)
        fig = self.build_figure(selected)

        event = st.plotly_chart(
            fig,
            width="stretch",
            on_select="rerun",
            key=self.chart_key,
        )

        if event and getattr(event, "selection", None) and event.selection.points:
            point = event.selection.points[0]

            original_idx = point.get("customdata")
            if original_idx is not None:
                new_selected = self._snap_from_original_index(int(original_idx))

                previous_selected = st.session_state.get(self.widget_key, self.default)
                if previous_selected != new_selected:
                    st.session_state[self.widget_key] = new_selected
                    st.rerun()

    def drawYourself(self) -> None:
        """A function to capture the selected peak and display it.

        Returns:
            _type_: It returns the user input but I'm not sure of the type.
        """
        selected = st.session_state.get(self.widget_key, self.default)
        if selected is None:
            st.info("Click a peak in the spectrum to select it.")
        else:
            st.write(f"Selected peak: **{selected:.3f} {self.type.unit}**")
        return selected

    def build_figure(self, selected_x: Optional[float] = None) -> go.Figure:
        """A function to build the plot.

        Args:
            selected_x (Optional[float], optional): x axis of the user input (I think). Defaults to None.

        Returns:
            go.Figure: The figure itself.
        """
        self._parse_jcampdx()
        fig = go.Figure()

        if self.type == SpectralType.MS:
            fig.add_trace(
                go.Bar(
                    x=self.display_x,
                    y=self.display_y,
                    customdata=self.display_idx,
                    showlegend=False,
                )
            )
        else:
            fig.add_trace(
                go.Scattergl(
                    x=self.display_x,
                    y=self.display_y,
                    mode="lines",
                    line=dict(width=1.5),
                    hoverinfo="skip",
                    showlegend=False,
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=self.display_x,
                    y=self.display_y,
                    mode="markers",
                    customdata=self.display_idx,
                    marker=dict(size=8, opacity=0.0),
                    hovertemplate="x=%{x}<extra></extra>",
                    showlegend=False,
                )
            )

        if selected_x is not None:
            fig.add_trace(
                go.Scatter(
                    x=[selected_x, selected_x],
                    y=[float(np.min(self.display_y)), float(np.max(self.display_y))],
                    mode="lines",
                    line=dict(color="red", width=2, dash="dash"),
                    showlegend=False,
                )
            )

        fig.update_layout(
            title=self.title,
            xaxis_title=self.units,
            yaxis_title=self.type.y_label,
            hovermode="closest",
            clickmode="event+select",
            dragmode="zoom",
            height=600,
        )

        if self.type == SpectralType.NMR:
            fig.update_layout(
                xaxis=dict(autorange="reversed"),
                yaxis=dict(visible=False),
            )

        return fig

    def _detect_type(self, imgpath: str) -> SpectralType:
        if re.search(r"ms", imgpath, re.IGNORECASE):
            return SpectralType.MS
        if re.search(r"ir", imgpath, re.IGNORECASE):
            return SpectralType.IR
        if re.search(r"nmr", imgpath, re.IGNORECASE):
            return SpectralType.NMR
        raise ValueError("Cannot determine spectral type")
