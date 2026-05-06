# ruff: noqua: F405
from importlib import import_module
from pathlib import Path
from sys import path as syspath

from checkers.BaseChecker import BaseChecker
from managers.BaseManager import BaseManager


class CheckerManager(BaseManager):
    """A manager for the custom checkers"""

    _item_dir = Path("checkers/")

    DEFAULT_CHECKERS = ["IntegerChecker"]

    @classmethod
    def buildChecker(cls, data: dict) -> BaseChecker:
        """Builds a checker based on the deserialised data object

        Args:
            data (dict): The dictionary with data

            Expects the following:
            - checkerType: string
            - checkerData: dict

        Raises:
            ValueError: Raised when the data is in the wrong shape

        Returns:
            BaseChecker: The checker built, can be any subclass of BaseChecker
        """
        checker_name = data.get("checkerType")
        checker_data = data.get("checkerData")
        if checker_name is None or checker_data is None:
            raise ValueError("Invalid checker!")
        cls.importChecker(checker_name)
        checker_type = BaseChecker.findChecker(checker_name)
        checker = checker_type.build(checker_data)
        return checker

    @classmethod
    def importChecker(cls, name: str) -> None:
        """Imports a checker from the data folder.

        It is important that all checkers are in a file with their own name.

        Args:
            name (str): The file to import from (and thus checker to load later)
        """
        if name in cls.DEFAULT_CHECKERS:
            return cls.importDefaultChecker(name)
        data_dir: str = str(cls._getDir().resolve())
        if data_dir not in syspath:
            syspath.append(data_dir)
        import_module(name)

    @classmethod
    def importDefaultChecker(cls, name: str) -> None:
        """Imports a checker from the checkers.default folder

        Args:
            name (str): The file to import from (and thus checker to load later)
        """
        import_module(f"checkers.default.{name}")
