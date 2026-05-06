import pathlib

from streamlit import cache_data

from managers.QuestionBuilder import QuestionBuilder
from managers.QuestionSerialiser import QuestionSerialiser
from questions.Question import Question


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
        question.figures = cls._resolveAssetPath(question.figures)
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
        manager_dir = current_file.parent
        src_dir = manager_dir.parent
        base_dir = src_dir.parent
        data_dir = base_dir.joinpath(cls._save_location).resolve()
        if not data_dir.exists():
            data_dir.mkdir(parents=True)
        return data_dir

    @classmethod
    def _getBaseDir(cls) -> pathlib.Path:
        """Return the repository root."""
        return pathlib.Path(__file__).resolve().parents[2]

    @classmethod
    def _resolveSingleAssetPath(cls, path: str) -> str:
        """Resolve a single asset path to an existing file when possible."""
        resolved_path = pathlib.Path(path)
        if resolved_path.is_absolute() and resolved_path.exists():
            return str(resolved_path)

        base_dir = cls._getBaseDir()
        question_dir = cls._getQuestionDir()
        data_root = base_dir / "data"

        candidates = [
            question_dir / resolved_path,
            base_dir / resolved_path,
            data_root / resolved_path,
            data_root / "images" / resolved_path.name,
            data_root / "molecules" / resolved_path.name,
            data_root / "spectra" / resolved_path.name,
            data_root / "spectra" / resolved_path,
        ]

        for candidate in candidates:
            if candidate.exists():
                return str(candidate.resolve())

        matches = list(data_root.rglob(resolved_path.name))
        if len(matches) == 1:
            return str(matches[0].resolve())

        return resolved_path

    @classmethod
    def _resolveAssetPath(cls, figures: dict | list[dict] | None) -> list[dict] | None:
        """Resolve question asset paths to existing files when possible."""
        if not figures:
            return None

        for figure in figures:
            figure["path"] = cls._resolveSingleAssetPath(figure["path"].strip())
        return figures or None
