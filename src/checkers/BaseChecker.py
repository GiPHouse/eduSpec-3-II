from abc import ABC, abstractmethod
from enum import Enum
from typing import Self, final

from questions.IntegerQuestion import IntegerQuestion
from questions.MoleculeDrawingQuestion import MoleculeDrawingQuestion
from questions.MultipleChoiceQuestion import MultipleChoiceQuestion
from questions.Question import Question
from questions.SpectralQuestion import SpectralQuestion
from questions.WordQuestion import WordQuestion


class CheckerTypes(Enum):
    """An enum for the question types a checker can check."""

    INTEGER = IntegerQuestion
    DRAWING = MoleculeDrawingQuestion
    MULTIPLECHOICE = MultipleChoiceQuestion
    SPECTRAL = SpectralQuestion
    WORD = WordQuestion


class BaseChecker(ABC):
    """The base class for all checkers. Implements some basic functions."""

    supported_questions = set()

    @final
    def __init__(self) -> None:
        """Initialises a general checker instance. DO NOT USE. This is only used for inheritance.

        To configure a base checker subclass, use `configureAvailableQuestions`
        """
        self._supported_questions = set()

    def supports_question(self, question: Question) -> bool:
        """Check whether this checker supports checking the given question.

        Args:
            question (Question): The question to check.

        Returns:
            bool: Whether this checker can check this type of question.
        """
        return question.__class__ in self._supported_questions

    @classmethod
    def build(cls, obj: dict) -> Self:
        """Builds a checker object.

        Args:
            object (dict): The json object to build from

        Returns:
            BaseChecker: The checker to build
        """
        out = cls()
        out.buildSelf(obj)
        return out

    @classmethod
    def serialise(cls, instance: Self) -> dict:
        """Serialises a checker object to put in json.

        Args:
            instance (Self): The checker to serialise

        Returns:
            dict: A dictionary with all the parameters stored in this checker. Will be fed into `build` to re-build this instance.
        """
        return instance.serialiseSelf()

    @abstractmethod
    def configureAvailableQuestions(self) -> None:
        """Add all question types this checker supports."""

    @abstractmethod
    def buildSelf(self, obj: dict) -> None:
        """Configures the checker.

        Args:
            object (dict): A parsed json dictionary built from `serialiseSelf`
        """
        pass

    @abstractmethod
    def serialiseSelf(self) -> dict:
        """Converts the checker to a dictionary for saving as json. Will be fed into `buildSelf` to set it up again.

        Returns:
            dict: The json-ready dictionary
        """
        pass
