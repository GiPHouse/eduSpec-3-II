import re
from enum import Enum
from typing import List, Optional

import jcamp
import numpy as np
import streamlit as st
from plotly import graph_objects as go

from questions.Question import Question


class SpectralType(Enum):
    """Enum type for types of different spectra

    Args:
        Enum (str,str,str): Spectra name, its unit and what the y-axis means.
    """

    MS = ("MS", "m/z", "Intensity")
    IR = ("IR", "cm^-1", "Transmittance")
    NMR = ("NMR", "ppm", "Intensity")

    def __init__(self, label: str, unit: str, y_label: str):
        """_summary_

        Args:
            label (_type_): Spectra name
            unit (_type_): Unit to measure spectra
            y_label (_type_): Wha the y-axis means
        """
        self.label = label
        self.unit = unit
        self.y_label = y_label


class SpectralQuestion(Question):
    """Class for Spectral Questions"""

    def __init__(
        self,
        name: str,
        title: str,
        bodytext: str,
        imgpath: Optional[str],
        correct_answer: float,
        feedbacks: List,
        tolerance: float = 0.5,
    ):
        """Function to initialize a spectral question instance

        Args:
            name (str): The unique name/ID of the question.
            title (str): Title of the Question
            bodytext (str): Bodytext, the question itself
            imgpath (Optional[str]): The path that points to the spectral data, to be displayed with the question
        """
        super().__init__(name, title, bodytext, imgpath)
        self.correct_answer = correct_answer
        self.tolerance = tolerance
        self.feedbacks = feedbacks
        self.widget_key = f"spectral_question_{name}"
        self.default = None
        self.type = self._detect_type(imgpath)

    def verifyAndFeedback(self, user_input: int) -> tuple[bool, str]:
        """Function that verifies the user input and gives feedback depending on the answer

        Args:
            user_input (int): The user input provided by the UI

        Returns:
            str: the feedback message
        """
        is_correct = abs(user_input - self.correct_answer) <= self.tolerance
        return is_correct, self.feedback(user_input)

    def feedback(self, user_input: int) -> str:
        """Gives the feedback depending on the user input

        Args:
            user_input (int): The user input provided by the UI

        Returns:
            str: the feedback message
        """
        if abs(user_input - self.correct_answer) <= self.tolerance:
            return self.feedbacks[0]
        return self.feedbacks[1]

    def _parse_jcampdx(self) -> None:
        """Parsing logic for JCAMP-DX files.

        Returns:
            tuple[list,list]: X and Y coordinate values, respectively.
        """
        # Return on no given file
        # ! Maybe make imgpath non-optional?
        if self.imgpath is None:
            return

        with open(self.imgpath, "rb") as f:
            lines = [ln.decode("utf-8", errors="replace") for ln in f.read().splitlines()]

        data = jcamp.jcamp_read(lines)

        x = np.asarray(data["x"], dtype=float)
        y = np.asarray(data["y"], dtype=float)

        if y.max() > 0:
            y = (y / y.max()) * 100
        self.units = data.get("xunits", "m/z")

        self.x = x
        self.y = y

    def drawYourself(self) -> None:
        """The question draws itself to streamlit"""
        selected = st.session_state.get(self.widget_key, self.default)
        if selected is not None:
            st.write(f"Selected peak: {selected} {self.type.unit}")
        else:
            st.info("Click a peak on the spectrum to select it.")
        return selected

    def drawImage(self) -> None:
        """We override the drawImage function as a spectral question needs to parse the spectral data"""
        self._parse_jcampdx()
        selected = st.session_state.get(self.widget_key, self.default)
        fig = self._build_figure(selected)

        event = st.plotly_chart(
            fig, use_container_width=True, on_select="rerun", key="spectral_chart"
        )

        if event and event.selection and event.selection.points:
            selected = event.selection.points[0]
            point_index = selected.get("point_index")
            if point_index is not None:
                selected_x = float(self.x[point_index])
                if st.session_state.get(self.widget_key) != selected_x:
                    st.session_state[self.widget_key] = selected_x
                    st.rerun()

    def _build_figure(self, selected_x: Optional[float] = None) -> go.Figure:
        """Create the Plotly figure for the current spectrum."""
        fig = go.Figure()

        if self.type == SpectralType.MS:
            fig.add_trace(
                go.Bar(
                    x=self.x,
                    y=self.y,
                    hovertemplate="%{{x:.1f}} {}<br>{}: %{{y:.2f}}<extra></extra>".format(
                        self.type.unit, self.type.y_label
                    ),
                    showlegend=False,
                )
            )

        else:
            fig.add_trace(
                go.Line(
                    x=self.x,
                    y=self.y,
                    mode="lines+markers",
                    line=dict(width=2),
                    marker=dict(size=8, opacity=0.0),  # invisible hit-targets
                    hovertemplate="%{{x:.1f}} {}<br>{}: %{{y:.2f}}<extra></extra>".format(
                        self.type.unit, self.type.y_label
                    ),
                    showlegend=False,
                )
            )

        if self.type == SpectralType.IR and selected_x is not None:
            fig.add_vline(
                x=selected_x,
                line_width=2,
                line_dash="dash",
                line_color="#d62728",
            )

        fig.update_layout(
            title=self.title,
            xaxis_title=self.units,
            yaxis_title=self.type.y_label,
            height=600,
            hovermode="closest",
        )

        return fig

    def _detect_type(self, imgpath: str) -> SpectralType:

        if re.search("^.*ms.*$", imgpath):
            return SpectralType.MS
        elif re.search("^.*ir.*$", imgpath):
            return SpectralType.IR

        # This doesn't work right now, up to how client created nmr files
        elif re.search("^.*nmr.*$", imgpath):
            return SpectralType.NMR

        raise ValueError("Not a proper spectral file is provided")
