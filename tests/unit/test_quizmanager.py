import pathlib

import pytest
from streamlit import cache_data

from managers.QuestionManager import QuestionManager
from managers.QuizManager import QuizManager
from questions.IntegerQuestion import IntegerQuestion
from Quiz import Quiz


class TestQuizManager:
    """Test cases for the quiz manager"""

    @pytest.fixture
    def tmp_question_path(self, tmp_path: pathlib.Path) -> pathlib.Path:
        """Creates a temporary question folder"""
        return tmp_path.joinpath("questions/")

    @pytest.fixture
    def tmp_quiz_path(self, tmp_path: pathlib.Path) -> pathlib.Path:
        """Creates a temporary quiz folder"""
        return tmp_path.joinpath("quizzes/")

    def test_saveLocation(
        self, tmp_question_path: pathlib.Path, tmp_quiz_path: pathlib.Path
    ) -> None:
        """Test case for changing the save location of both question and quiz managers"""
        QuestionManager._save_location = tmp_question_path  # noqa: SLF001
        QuizManager._save_location = tmp_quiz_path  # noqa: SLF001
        cache_data.clear()

        assert QuestionManager._getQuestionDir() == tmp_question_path  # noqa: SLF001
        assert QuizManager._getQuizDir() == tmp_quiz_path  # noqa: SLF001
        assert tmp_question_path != tmp_quiz_path

    def test_saveQuiz(self, tmp_quiz_path: pathlib.Path) -> None:
        """Test case for saving a simple quiz"""
        QuizManager._save_location = tmp_quiz_path  # noqa: SLF001
        cache_data.clear()

        intq = IntegerQuestion(
            "question1",
            "Example Question",
            "here's a question",
            (0, 3),
            ["correct", "too low", "too high"],
        )

        quiz1 = Quiz("quiz1", [intq])

        assert QuizManager.saveQuiz(quiz1)

        expected_location = tmp_quiz_path.joinpath("quiz1.json")

        assert expected_location.is_file()

        found_data = expected_location.read_text()

        assert found_data == r"""{"id": "quiz1", "questionNames": ["question1"]}"""

    def test_loadQuiz(self, tmp_quiz_path: pathlib.Path, tmp_question_path: pathlib.Path) -> None:
        """Test case for loading a simple quiz"""
        QuestionManager._save_location = tmp_question_path  # noqa: SLF001
        QuizManager._save_location = tmp_quiz_path  # noqa: SLF001
        cache_data.clear()

        intq = IntegerQuestion(
            "question1",
            "Example Question",
            "here's a question",
            (0, 3),
            ["correct", "too low", "too high"],
        )
        QuestionManager.saveQuestion(intq)

        expected_location = tmp_quiz_path.joinpath("quiz2.json")
        assert not expected_location.exists()
        assert not tmp_quiz_path.exists()
        tmp_quiz_path.mkdir(parents=True)

        expected_location.touch()
        expected_location.write_text(r"""{"id": "quiz2", "questionNames": ["question1"]}""")

        built_quiz = QuizManager.loadQuiz("quiz2")

        assert isinstance(built_quiz, Quiz)

        assert built_quiz.name == "quiz2"
        assert len(built_quiz.question_list) == 1

        built_question = built_quiz.question_list[0]

        assert isinstance(built_question, IntegerQuestion)

        assert built_question.name == intq.name
        assert built_question.title == intq.title
        assert built_question.bodytext == intq.bodytext
        assert built_question.figures == intq.figures
        assert built_question.correct_answer == intq.correct_answer
        assert built_question.feedbacks == intq.feedbacks

    def test_updateQuiz(self, tmp_quiz_path: pathlib.Path) -> None:
        """Test case for updating a simple quiz"""
        QuizManager._save_location = tmp_quiz_path  # noqa: SLF001
        cache_data.clear()

        quiz1 = Quiz(
            "quiz1",
            [IntegerQuestion("question1", "title", "bodytext", (0, 3), ["right", "low", "high"])],
        )

        QuizManager.saveQuiz(quiz1)

        quiz2 = Quiz(
            "quiz1",
            [IntegerQuestion("question2", "title", "bodytext", (0, 3), ["right", "low", "high"])],
        )

        QuizManager.updateQuiz(quiz2)

        expected_location = tmp_quiz_path.joinpath("quiz1.json")

        assert expected_location.is_file()

        found_data = expected_location.read_text()

        assert found_data == r"""{"id": "quiz1", "questionNames": ["question2"]}"""

    def test_LoadQuiz_nonExistent(self, tmp_quiz_path: pathlib.Path) -> None:
        """Test case for loading a non-existent quiz"""
        QuizManager._save_location = tmp_quiz_path  # noqa: SLF001
        cache_data.clear()

        expected_location = tmp_quiz_path.joinpath("doesnotexist.json")
        assert not expected_location.exists()

        with pytest.raises(FileNotFoundError):
            assert isinstance(QuizManager.loadQuiz("doesnotexist"), Quiz)

    def test_SaveQuiz_duplicate(self, tmp_quiz_path: pathlib.Path) -> None:
        """Test case for saving a quiz name that already exists"""
        QuizManager._save_location = tmp_quiz_path  # noqa: SLF001
        cache_data.clear()

        quiz1 = Quiz(
            "quiz1",
            [IntegerQuestion("question1", "title", "bodytext", (0, 3), ["right", "low", "high"])],
        )
        assert QuizManager.saveQuiz(quiz1)

        expected_location = tmp_quiz_path.joinpath("quiz1.json")
        assert expected_location.is_file()

        quiz2 = Quiz(
            "quiz1",
            [IntegerQuestion("question2", "title", "bodytext", (0, 3), ["right", "low", "high"])],
        )

        with pytest.raises(FileExistsError):
            assert QuizManager.saveQuiz(quiz2)
