from typing import List, Optional

import jcamp
import numpy as np
import streamlit as st
from plotly import graph_objects as go

from Question import Question


class SpectralQuestion(Question):
    """Class for Spectral Questions"""

    def __init__(
        self,
        title: str,
        bodytext: str,
        imgpath: Optional[str],
        correct_mz: float,
        feedbacks: List,
        tolerance: float = 0.5,
    ):
        """Function to initialize a spectral question instance

        Args:
            title (str): Title of the Question
            bodytext (str): Bodytext, the question itself
            imgpath (Optional[str]): The path that points to the spectral data, to be displayed with the question
        """
        super().__init__(title, bodytext, imgpath)
        self.correct_mz = correct_mz
        self.tolerance = tolerance
        self.feedbacks = feedbacks
        self.widget_key = "spectral_question"
        self.default = None

    def verifyAndFeedback(self, user_input: int) -> str:
        """Function that verifies the user input and gives feedback depending on the answer

        Args:
            user_input (int): The user input provided by the UI

        Returns:
            str: the feedback message
        """
        is_correct = abs(user_input - self.correct_mz) <= self.tolerance
        return is_correct, self.feedback(user_input)

    def feedback(self, user_input: int) -> str:
        """Gives the feedback depending on the user input

        Args:
            user_input (int): The user input provided by the UI

        Returns:
            str: the feedback message
        """
        if abs(user_input - self.correct_mz) <= self.tolerance:
            return self.feedbacks[0]
        return self.feedbacks[1]

    def _parse_jcampdx(self) -> None:
        """Parsing logic for JCAMP-DX files.

        Returns:
            tuple[list,list]: X and Y coordinate values, respecitvely.
        """
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
            st.write(f"**Selected peak:** m/z = {selected}")
        else:
            st.info("Click a peak on the spectrum to select it.")
        return selected

    def drawImage(self) -> None:
        """We override the drawImage function as a spectral question needs to parse the spectral data"""
        self._parse_jcampdx()

        # This is a weird numpy trick so that we can easily create a "stem" plot.
        xs = np.empty(self.x.size * 3)
        ys = np.empty(self.y.size * 3)

        xs[0::3] = self.x
        xs[1::3] = self.x
        xs[2::3] = np.nan

        ys[0::3] = 0
        ys[1::3] = self.y
        ys[2::3] = np.nan
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=xs, y=ys, mode="lines", line=dict(width=1), hoverinfo="skip", showlegend=False
            )
        )

        # peak tops
        fig.add_trace(
            go.Scatter(
                x=self.x,
                y=self.y,
                mode="markers",
                marker=dict(size=6),
                hovertemplate="m/z: %{x}<br>Intensity: %{y:.2f}<extra></extra>",
                showlegend=False,
            )
        )

        fig.update_layout(
            title=self.title,
            xaxis_title=self.units,
            yaxis_title="Relative abundance (%)",
            height=600,
            hovermode="closest",
        )

        event = st.plotly_chart(
            fig, use_container_width=True, on_select="rerun", key="spectral_chart"
        )

        if event and event.selection and event.selection.points:
            selected = event.selection.points[0]
            point_index = selected.get("point_index")
            if point_index is not None:
                st.session_state[self.widget_key] = float(self.x[point_index])
