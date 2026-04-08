import pathlib

import pytest
from streamlit import cache_data

from managers.BaseManager import BaseManager
from managers.QuestionManager import QuestionManager
from managers.QuizManager import QuizManager
from questions.IntegerQuestion import IntegerQuestion
from Quiz import Quiz


class TestQuizManager:
    """Test cases for the quiz manager"""

    def test_saveLocation(self, tmp_path: pathlib.Path) -> None:
        """Test case for changing the save location of both question and quiz managers"""
        BaseManager._data_dir = tmp_path  # noqa : SLF001
        cache_data.clear()

        assert QuestionManager._getDir() == tmp_path.joinpath(QuestionManager._item_dir)  # noqa: SLF001
        assert QuizManager._getDir() == tmp_path.joinpath(QuizManager._item_dir)  # noqa: SLF001

    def test_saveQuiz(self, tmp_path: pathlib.Path) -> None:
        """Test case for saving a simple quiz"""
        BaseManager._data_dir = tmp_path  # noqa : SLF001
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

        expected_location = tmp_path.joinpath(QuizManager._item_dir).joinpath("quiz1.json")  # noqa: SLF001

        assert expected_location.is_file()

        found_data = expected_location.read_text()

        assert found_data == r"""{"id": "quiz1", "questionNames": ["question1"]}"""

    def test_loadQuiz(
        self,
        tmp_path: pathlib.Path,
    ) -> None:
        """Test case for loading a simple quiz"""
        BaseManager._data_dir = tmp_path  # noqa : SLF001
        cache_data.clear()

        intq = IntegerQuestion(
            "question1",
            "Example Question",
            "here's a question",
            (0, 3),
            ["correct", "too low", "too high"],
        )
        QuestionManager.saveQuestion(intq)

        expected_location = tmp_path.joinpath(QuizManager._item_dir).joinpath("quiz2.json")  # noqa: SLF001
        assert not expected_location.exists()
        expected_location.parent.mkdir(parents=True, exist_ok=True)

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
        assert built_question.imgpath == intq.imgpath
        assert built_question.correct_answer == intq.correct_answer
        assert built_question.feedbacks == intq.feedbacks

    def test_updateQuiz(self, tmp_path: pathlib.Path) -> None:
        """Test case for updating a simple quiz"""
        BaseManager._data_dir = tmp_path  # noqa : SLF001
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

        expected_location = tmp_path.joinpath(QuizManager._item_dir).joinpath("quiz1.json")  # noqa: SLF001

        assert expected_location.is_file()

        found_data = expected_location.read_text()

        assert found_data == r"""{"id": "quiz1", "questionNames": ["question2"]}"""

    def test_LoadQuiz_nonExistent(self, tmp_path: pathlib.Path) -> None:
        """Test case for loading a non-existent quiz"""
        BaseManager._data_dir = tmp_path  # noqa : SLF001
        cache_data.clear()

        expected_location = tmp_path.joinpath(QuizManager._item_dir).joinpath("doesnotexist.json")  # noqa: SLF001
        assert not expected_location.exists()

        with pytest.raises(FileNotFoundError):
            assert isinstance(QuizManager.loadQuiz("doesnotexist"), Quiz)

    def test_SaveQuiz_duplicate(self, tmp_path: pathlib.Path) -> None:
        """Test case for saving a quiz name that already exists"""
        BaseManager._data_dir = tmp_path  # noqa : SLF001
        cache_data.clear()

        quiz1 = Quiz(
            "quiz1",
            [IntegerQuestion("question1", "title", "bodytext", (0, 3), ["right", "low", "high"])],
        )
        assert QuizManager.saveQuiz(quiz1)

        expected_location = tmp_path.joinpath(QuizManager._item_dir).joinpath("quiz1.json")  # noqa: SLF001
        assert expected_location.is_file()

        quiz2 = Quiz(
            "quiz1",
            [IntegerQuestion("question2", "title", "bodytext", (0, 3), ["right", "low", "high"])],
        )

        with pytest.raises(FileExistsError):
            assert QuizManager.saveQuiz(quiz2)
