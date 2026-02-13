from typing import Optional

from Question import Question


class SpectralQuestion(Question):
    """The spectral-selection question class. Currently not fully implemented."""

    def __init__(self, title: str, bodytext: str, imgpath: Optional[str] = None):
        """Initialises a spectral-selection question

        Args:
            title (str): The title of the question.
            bodytext (str): The body text of the question.
            imgpath (Optional[str], optional): Path to the image used for the question. Defaults to None.
        """
        super().__init__(title, bodytext, imgpath)

    def verifyAndFeedback(self, user_input: int) -> None:
        """Interface template. Returns whether an answer is correct and the feedback given."""
        pass

    def feedback(self, user_input: int) -> None:
        """Interface template. Returns the feedback for an answer."""
        pass
