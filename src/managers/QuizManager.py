import json
from pathlib import Path

from streamlit import cache_data

from managers.BaseManager import BaseManager
from managers.QuestionManager import QuestionManager
from managers.QuizBuilder import QuizBuilder
from managers.QuizSerialiser import QuizSerialiser
from Quiz import Quiz
from validators.quizValidation import validateQuiz, validateQuizObject


class QuizManager(BaseManager):
    """Class for loading quizzes from/to the file system"""

    _item_dir = Path("quizzes")

    @classmethod
    @cache_data
    def loadQuiz(cls, name: str) -> Quiz | None:
        """Loads a quiz from its name.

        Will also load all of the questions within said quiz.

        Args:
            name (str): The unique id/name of the quiz to load.

        Raises:
            FileNotFound: When trying to load a quiz or question that doesn't exist.
            TypeError: When building an unrecognised question type.
            ValueError: When building a malformed quiz or question.

        Returns:
            Quiz: The quiz.
        """
        if not cls.itemExists(name):
            return None

        data_dir = cls._getDir()
        quiz_file = data_dir.joinpath(f"{name}.json")

        quiz_data = quiz_file.read_text()

        quiz = QuizBuilder.quizFromJson(quiz_data)
        return quiz

    @classmethod
    def saveQuiz(cls, quiz: Quiz) -> bool:
        """Saves a quiz to the file system. Use `updateQuiz()` to change an existing one.

        Will not save the questions. Do this separately.

        Raises:
            FileExistsError: When trying to save a duplicate quiz.

        Args:
            quiz (Quiz): The quiz to save.

        Returns:
            bool: Whether saving was succesful.
        """
        quiz_name = quiz.name

        if cls.itemExists(quiz_name):
            raise FileExistsError(f"Quiz {quiz_name} already exists!")

        quiz_data = QuizSerialiser.quizToJson(quiz)

        data_dir = cls._getDir()
        quiz_file = data_dir.joinpath(f"{quiz_name}.json")
        quiz_file.write_text(quiz_data)
        return True

    @classmethod
    def updateQuiz(cls, quiz: Quiz) -> bool:
        """Updates an existing quiz. Use `saveQuiz()` for a new one.

        Will not update the questions. Do this separately.

        Raises:
            FileNotFoundError: When the quiz doesn't exist yet.

        Returns:
            bool: Whether updating was succesful.
        """
        quiz_name = quiz.name
        if not cls.itemExists(quiz_name):
            raise FileNotFoundError(f"Quiz {quiz_name} does not exist!")

        quiz_data = QuizSerialiser.quizToJson(quiz)

        data_dir = cls._getDir()
        quiz_file = data_dir.joinpath(f"{quiz_name}.json")
        quiz_file.write_text(quiz_data)
        return True

    @classmethod
    def validateQuiz(cls, name: str) -> list[str]:
        """Validates a quiz based on its name.

        Args:
            name (str): The unique id/name of the quiz to check.

        Returns:
            list[str]: A list of problems. If there are none the quiz is valid.
        """
        if not cls.itemExists(name):
            return [f"There exists no quiz with the name {name}."]

        data_dir = cls._getDir()
        quiz_file = data_dir.joinpath(f"{name}.json")

        quiz_data = quiz_file.read_text()

        return validateQuiz(quiz_data, file_name=quiz_file)

    @classmethod
    def validateQuizRecursive(cls, name: str) -> tuple[list[str], dict[str, list[str]]]:
        """Validates a quiz an all its questions based on its name.

        Args:
            name (str): The unique id/name of the quiz to check.

        Returns:
            list[str],dict[str,list[str]]: A list of problems, and a dict with all question names and the list of their problems. If all of these are empty the quiz and its questions are valid.
        """
        if not cls.itemExists(name):
            return ([f"There exists no quiz with the name {name}."], {})

        data_dir = cls._getDir()
        quiz_file = data_dir.joinpath(f"{name}.json")

        quiz_data = quiz_file.read_text()

        quiz_obj = json.loads(quiz_data)

        problems = validateQuizObject(quiz_obj, file_name=f"{name}.json")

        attr_questions = quiz_obj.get("questionNames", [])
        if not isinstance(attr_questions, list):
            return problems, {}

        question_problems = {}
        for question in attr_questions:
            question_problems[question] = QuestionManager.validateQuestion(question)

        return problems, question_problems

    @classmethod
    def listQuizzes(cls) -> list[str]:
        """Lists all saved quizzes. Ignores subdirectories.

        Returns:
            list[str]: The found items.
        """
        base_dir = cls._getDir()

        found_items = cls._iterDir(base_dir, False)

        # Useless iteration but required for typing
        out = [x for x in found_items if isinstance(x, str)]

        return out
