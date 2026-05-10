import pathlib

import pytest
from streamlit import cache_data

from managers.QuestionManager import QuestionManager
from managers.QuizBuilder import QuizBuilder
from questions.IntegerQuestion import IntegerQuestion
from Quiz import Quiz


class TestQuizBuilder:
    """Test cases for the quiz builder"""

    def test_quizBuild_1(self, tmp_path: pathlib.Path) -> None:
        """Test case for simple quiz building"""
        QuestionManager._save_location = tmp_path  # noqa: SLF001
        cache_data.clear()

        input_data = r"""{"id": "quiz1", "questionNames": ["question1"]}"""

        correct_question = IntegerQuestion(
            "question1", "title", "btext", (2, 3), ["right", "low", "high"]
        )

        QuestionManager.saveQuestion(correct_question)

        built_quiz = QuizBuilder.quizFromJson(input_data)

        assert built_quiz.name == "quiz1"
        assert len(built_quiz.question_list) == 1

        built_question = built_quiz.question_list[0]

        assert isinstance(built_question, IntegerQuestion)

        assert built_question.name == correct_question.name
        assert built_question.title == correct_question.title
        assert built_question.bodytext == correct_question.bodytext
        assert built_question.figures == correct_question.figures
        assert built_question.correct_answer == correct_question.correct_answer
        assert built_question.feedbacks == correct_question.feedbacks

    def test_quizBuild_faulty_1(self) -> None:
        """Test case for building a quiz without id attribute"""
        input_data = r"""{"questionNames": ["question1"]}"""

        with pytest.raises(ValueError):
            assert isinstance(QuizBuilder.quizFromJson(input_data), Quiz)

    def test_quizBuild_faulty_2(self) -> None:
        """Test case for building a quiz without questions"""
        input_data = r""""{"id": "quiz1", "questionNames": []}"""

        with pytest.raises(ValueError):
            assert isinstance(QuizBuilder.quizFromJson(input_data), Quiz)

    def test_quizBuild_faulty_3(self, tmp_path: pathlib.Path) -> None:
        """Test case for building a quiz with a non-existent question"""
        QuestionManager._save_location = tmp_path  # noqa: SLF001
        cache_data.clear()

        input_data = r"""{"id": "quiz1", "questionNames": ["question1"]}"""

        with pytest.raises(ValueError):
            assert isinstance(QuizBuilder.quizFromJson(input_data), Quiz)
