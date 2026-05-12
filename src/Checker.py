from collections.abc import Callable


class Checker:
    """Wrapper class for custom checkers"""

    def __init__(self, checking_function: Callable) -> None:
        """Initialises a checker object

        Args:
            checking_function (function): The function that will be used for checking.
        """
        self.check = checking_function
