from typing import Optional

import jcamp
import numpy as np

from Question import Question


class SpectralQuestion(Question):
    """Class for Spectral Questions
    """

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

    def parse_jcampdx(self) -> tuple[list, list]:
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

        return (x, y)
