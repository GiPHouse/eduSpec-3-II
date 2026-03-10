import pathlib

from streamlit import cache_data

from Question import Question
from QuestionBuilder import QuestionBuilder
from QuestionSerialiser import QuestionSerialiser


class QuestionManager:
    """Class for loading questions from/to the file system"""

    # Here to be modified during tests.
    # DO NOT ACTUALLY EDIT
    _save_location = pathlib.Path("data/questions/")

    @classmethod
    @cache_data
    def loadQuestion(cls, name: str) -> Question:
        """Loads a question from its name.

        Args:
            name (str): The unique id/name of the question to load.

        Raises:
            FileNotFound: When trying to load a question that doesn't exist.
            TypeError: When building an unrecognised question type.
            ValueError: When building a malformed question.

        Returns:
            Question: The question.
        """
        if not cls.questionExists(name):
            raise FileNotFoundError(f"Question {name} does not exist!")

        data_dir = cls._getQuestionDir()
        question_file = data_dir.joinpath(f"{name}.json")

        question_data = question_file.read_text()

        question = QuestionBuilder.questionFromJson(question_data)
        return question

    @classmethod
    def saveQuestion(cls, question: Question) -> bool:
        """Saves a question to the file system. Use `updateQuestion()` to change an existing one.

        Raises:
            FileExistsError: When trying to save a duplicate question.

        Args:
            question (Question): The question to save.

        Returns:
            bool: Whether saving was succesful.
        """
        question_name = question.name

        if cls.questionExists(question_name):
            raise FileExistsError(f"Question {question_name} already exists!")

        question_data = QuestionSerialiser.questionToJson(question)

        data_dir = cls._getQuestionDir()
        question_file = data_dir.joinpath(f"{question_name}.json")
        question_file.write_text(question_data)
        return True

    @classmethod
    def updateQuestion(cls, question: Question) -> bool:
        """Updates an existing question. Use `saveQuestion()` for a new one.

        Raises:
            FileNotFoundError: When the question doesn't exist yet.

        Returns:
            bool: Whether updating was succesful.
        """
        question_name = question.name
        if not cls.questionExists(question_name):
            raise FileNotFoundError(f"Question {question_name} does not exist!")

        question_data = QuestionSerialiser.questionToJson(question)

        data_dir = cls._getQuestionDir()
        question_file = data_dir.joinpath(f"{question_name}.json")
        question_file.write_text(question_data)
        return True

    @classmethod
    def questionExists(cls, name: str) -> bool:
        """Checks whether a question with the given name is currently saved

        Args:
            name (str): The unique id/name of the question to verify

        Returns:
            bool: Whether the question exists on the system
        """
        data_dir = cls._getQuestionDir()

        question_file = data_dir.joinpath(f"{name}.json")

        return question_file.is_file()

    @classmethod
    def _getQuestionDir(cls) -> pathlib.Path:
        """Returns the question directory path

        Returns:
            pathlib.Path: The question directory path
        """
        current_file = pathlib.Path(__file__)
        src_dir = current_file.parent
        base_dir = src_dir.parent
        data_dir = base_dir.joinpath(cls._save_location).resolve()
        if not data_dir.exists():
            data_dir.mkdir(parents=True)
        return data_dir
