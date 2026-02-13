from typing import Optional

from Question import Question


class SpectralQuestion(Question):
    """_summary_

    Args:
        Question (_type_): _description_
    """

    def __init__(self, title: str, bodytext: str, imgpath: Optional[str] = None):
        """_summary_

        Args:
            title (str): _description_
            bodytext (str): _description_
            imgpath (Optional[str], optional): _description_. Defaults to None.
        """
        super().__init__(title, bodytext, imgpath)

    def verifyAndFeedback(self, user_input: int) -> tuple[bool, str]:
        """_summary_

        Args:
            user_input (int): _description_

        Returns:
            Tuple[bool, str]: _description_
        """
        pass

    def feedback(self, user_input: int) -> str:
        """_summary_

        Args:
            user_input (int): _description_

        Returns:
            str: _description_
        """
        pass
