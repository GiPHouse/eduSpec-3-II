import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

from Question import Question
from SpectralQuestion import SpectralQuestion


class QuestionDrawer:
    """Public class for displaying questions"""

    @staticmethod
    def drawQuestion(current_question: Question) -> None:
        """Function to display a question, independent of its subtype

        Args:
            current_question (Question): The Question to be displayed

        Returns:
            _type_: Probably a Streamlit object or nothing. Depends on our design choice. (Not complete yet)
        """
        pio.templates.default = "plotly_white"  # consistent light

        if isinstance(current_question, SpectralQuestion):
            pass

        if isinstance(current_question, SpectralQuestion):
            """
            Parses the specified JCAMP-DX file. This file is specified in the imgpath field.
            Returns the parsed data as a plotly "stem" figure.

            """
            x, y = current_question.parse_jcampdx()

            # This is a weird numpy trick so that we can easily create a "stem" plot.
            xs = np.empty(x.size * 3)
            ys = np.empty(y.size * 3)

            xs[0::3] = x
            xs[1::3] = x
            xs[2::3] = np.nan

            ys[0::3] = 0
            ys[1::3] = y
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
                    x=x,
                    y=y,
                    mode="markers",
                    marker=dict(size=6),
                    hovertemplate="m/z: %{x}<br>Intensity: %{y:.2f}<extra></extra>",
                    showlegend=False,
                )
            )

            fig.update_layout(
                title=current_question.title,
                xaxis_title=current_question.units,
                yaxis_title="Relative abundance (%)",
                height=600,
                hovermode="closest",
            )

            return fig
