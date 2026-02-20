from typing import Optional

import jcamp
import numpy as np
import streamlit as st
from plotly import graph_objects as go

from Question import Question


class SpectralQuestion(Question):
    """Class for Spectral Questions"""

    def __init__(self, title: str, bodytext: str, imgpath: Optional[str]):
        """Function to initialize a spectral question instance

        Args:
            title (str): Title of the Question
            bodytext (str): Bodytext, the question itself
            imgpath (Optional[str]): The path that points to the spectral data, to be displayed with the question
        """
        super().__init__(title, bodytext, imgpath)

    def verifyAndFeedback(self, user_input: int) -> str:
        """Function that verifies the user input and gives feedback depending on the answer

        Args:
            user_input (int): The user input provided by the UI

        Returns:
            str: the feedback message
        """
        pass

    def feedback(user_input: int) -> str:
        """Gives the feedback depending on the user input

        Args:
            user_input (int): The user input provided by the UI

        Returns:
            str: the feedback message
        """
        pass

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
        pass

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

        st.plotly_chart(fig, use_container_width=True)
