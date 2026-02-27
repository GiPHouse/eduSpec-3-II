from Quiz import Quiz
from QuizSerialiser import QuizSerialiser
from WordQuestion import WordQuestion


class test_QuizSerialisation:
    """Test cases for quiz serialisation"""

    def test_simpleQuiz(self) -> None:
        """Test case for a simple quiz"""
        quiz = Quiz(
            "quiz1", [WordQuestion("question1", "Question", "Text", "answer", ["correct", "false"])]
        )

        j = QuizSerialiser.quizToJson(quiz)

        assert j == rf"""{"name": "quiz1", "questionNames": ["question1"]}"""
