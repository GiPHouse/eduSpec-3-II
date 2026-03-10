import pathlib

from streamlit import cache_data

from managers.QuestionManager import QuestionManager
from managers.QuizBuilder import QuizBuilder
from managers.QuizSerialiser import QuizSerialiser
from questions.IntegerQuestion import IntegerQuestion
from Quiz import Quiz


class Test_QuizSerialisationCycle:
    """Test cases for quiz serialisation cycling"""

    def test_quizCycle(self, tmp_path: pathlib.Path) -> None:
        """Test case for quiz serialisation cycling"""
        QuestionManager._save_location = tmp_path  # noqa: SLF001
        cache_data.clear()

        intq = IntegerQuestion(
            "question1",
            "Example Question",
            "here's a question",
            (0, 3),
            ["correct", "too low", "too high"],
        )

        quiz = Quiz("quiz1", [intq])

        QuestionManager.saveQuestion(intq)

        json_1 = QuizSerialiser.quizToJson(quiz)

        quiz_built = QuizBuilder.quizFromJson(json_1)

        json_2 = QuizSerialiser.quizToJson(quiz_built)

        assert json_1 == json_2
