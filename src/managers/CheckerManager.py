# ruff: noqua: F405
from collections.abc import Callable
from importlib import import_module
from pathlib import Path
from sys import path as syspath
from types import ModuleType

from Checker import Checker
from managers.BaseManager import BaseManager


class CheckerManager(BaseManager):
    """A manager for the custom checkers"""

    _item_dir = Path("checkers/")

    DEFAULT_CHECKERS = ["IntegerChecker"]

    @classmethod
    def buildChecker(cls, name: str) -> Checker:
        """Builds a checker based on the module name.

        Args:
            name (str): The name of the checker file. Must contain a proper check() function. Does not need to end in .py.

        Raises:
            FileNotFoundError: Raised when the checker isn't found.

        Returns:
            Checker: The checker built
        """
        checking_function = cls._importChecker(name)
        checker = Checker(checking_function, name)
        return checker

    @classmethod
    def _importChecker(cls, name: str) -> Callable:
        """Imports a checker from the data folder.

        It is important that all checkers are in a file with their own name.

        Args:
            name (str): The file to import from (and thus checker to load later)
        """
        data_dir: str = str(cls._getDir().resolve())
        if data_dir not in syspath:
            syspath.append(data_dir)
        checker_file = import_module(name)
        if not cls._validateChecker(checker_file):
            raise NameError("No function `check(answer) -> tuple[bool, str]` found")
        return checker_file.check

    @classmethod
    def _validateChecker(cls, checker_file: ModuleType) -> bool:
        """Checks whether the checker file contains a proper check function.

        The function should have the annotation `check(answer) -> tuple[bool, str]`.

        Args:
            checker_file (ModuleType): The module to check.

        Returns:
            bool: Whether a proper check function is present.
        """
        try:
            check_function = checker_file.check
            if not isinstance(check_function, Callable):
                return False
            annotations = check_function.__annotations__
            if annotations.get("return", "") != tuple[bool, str]:
                return False
            if len(annotations) != 2:
                return False
            return True
        except Exception:
            return False
