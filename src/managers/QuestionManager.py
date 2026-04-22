from pathlib import Path

from streamlit import cache_data

from managers.BaseManager import BaseManager, DirectoryStructure
from managers.QuestionBuilder import QuestionBuilder
from managers.QuestionSerialiser import QuestionSerialiser
from questions.Question import Question


class QuestionManager(BaseManager):
    """Class for loading questions from/to the file system"""

    _item_dir = Path("questions/")

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
        if not cls.itemExists(name):
            raise FileNotFoundError(f"Question {name} does not exist!")

        data_dir = cls._getDir()
        question_file = data_dir.joinpath(f"{name}.json")

        question_data = question_file.read_text()

        question = QuestionBuilder.questionFromJson(question_data)
        question.imgpath = cls._resolveAssetPath(question.imgpath)
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

        if cls.itemExists(question_name):
            raise FileExistsError(f"Question {question_name} already exists!")

        question_data = QuestionSerialiser.questionToJson(question)

        data_dir = cls._getDir()
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
        if not cls.itemExists(question_name):
            raise FileNotFoundError(f"Question {question_name} does not exist!")

        question_data = QuestionSerialiser.questionToJson(question)

        data_dir = cls._getDir()
        question_file = data_dir.joinpath(f"{question_name}.json")
        question_file.write_text(question_data)
        return True

    @classmethod
    def listQuestions(cls) -> DirectoryStructure:
        """Lists all the currently saved questions

        Returns:
            DirectoryStructure: The question ids. Subdirectories are tuples with the dir name first and list of questions second.
        """
        base_dir = cls._getDir()

        return cls._iterDir(base_dir)

    @classmethod
    def _resolveSingleAssetPath(cls, imgpath: str) -> str:
        """Resolve a single asset path to an existing file when possible."""
        path = Path(imgpath)
        if path.is_absolute() and path.exists():
            return str(path)

        base_dir = cls._getDir().parent
        question_dir = cls._getDir()
        data_root = base_dir / "data"

        candidates = [
            question_dir / path,
            base_dir / path,
            data_root / path,
            data_root / "images" / path.name,
            data_root / "molecules" / path.name,
            data_root / "spectra" / path.name,
            data_root / "spectra" / path,
        ]

        for candidate in candidates:
            if candidate.exists():
                return str(candidate.resolve())

        matches = list(data_root.rglob(path.name))
        if len(matches) == 1:
            return str(matches[0].resolve())

        return imgpath

    @classmethod
    def _resolveAssetPath(
        cls, imgpath: str | list[str] | tuple[str, ...] | None
    ) -> list[str] | None:
        """Resolve question asset paths to existing files when possible."""
        if not imgpath:
            return None

        if isinstance(imgpath, str):
            cleaned = imgpath.strip()
            if not cleaned:
                return None
            return [cls._resolveSingleAssetPath(cleaned)]

        resolved_paths = [
            cls._resolveSingleAssetPath(path.strip())
            for path in imgpath
            if isinstance(path, str) and path.strip()
        ]
        return resolved_paths or None
