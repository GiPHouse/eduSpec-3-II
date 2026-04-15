import pathlib

from streamlit import cache_data

from managers.QuizBuilder import QuizBuilder
from managers.QuizSerialiser import QuizSerialiser
from Quiz import Quiz


class QuizManager:
    """Class for loading quizzes from/to the file system"""

    # Here to be modified during tests.
    # DO NOT ACTUALLY EDIT
    _save_location = pathlib.Path("data/quizzes/")

    @classmethod
    @cache_data
    def loadQuiz(cls, name: str) -> Quiz:
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
        if not cls.quizExists(name):
            raise FileNotFoundError(f"Quiz {name} does not exist!")

        data_dir = cls._getQuizDir()
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

        if cls.quizExists(quiz_name):
            raise FileExistsError(f"Quiz {quiz_name} already exists!")

        quiz_data = QuizSerialiser.quizToJson(quiz)

        data_dir = cls._getQuizDir()
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
        if not cls.quizExists(quiz_name):
            raise FileNotFoundError(f"Quiz {quiz_name} does not exist!")

        quiz_data = QuizSerialiser.quizToJson(quiz)

        data_dir = cls._getQuizDir()
        quiz_file = data_dir.joinpath(f"{quiz_name}.json")
        quiz_file.write_text(quiz_data)
        return True

    @classmethod
    def quizExists(cls, name: str) -> bool:
        """Checks whether a quiz with the given name is currently saved

        Args:
            name (str): The unique id/name of the quiz to verify

        Returns:
            bool: Whether the quiz exists on the system
        """
        data_dir = cls._getQuizDir()

        quiz_file = data_dir.joinpath(f"{name}.json")

        return quiz_file.is_file()

    @classmethod
    def _getQuizDir(cls) -> pathlib.Path:
        """Returns the quiz directory path

        Returns:
            pathlib.Path: The quiz directory path
        """
        current_file = pathlib.Path(__file__)
        manager_dir = current_file.parent
        src_dir = manager_dir.parent
        base_dir = src_dir.parent
        data_dir = base_dir.joinpath(cls._save_location).resolve()
        if not data_dir.exists():
            data_dir.mkdir(parents=True)
        return data_dir
