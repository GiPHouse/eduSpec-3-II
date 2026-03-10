from managers.QuizSerialiser import QuizSerialiser
from questions.IntegerQuestion import IntegerQuestion
from questions.MultipleChoiceQuestion import MultipleChoiceQuestion
from questions.WordQuestion import WordQuestion
from Quiz import Quiz


class test_QuizSerialisation:
    """Test cases for quiz serialisation"""

    def test_simpleQuiz(self) -> None:
        """Test case for a simple quiz"""
        quiz = Quiz(
            "quiz1", [WordQuestion("question1", "Question", "Text", "answer", ["correct", "false"])]
        )

        j = QuizSerialiser.quizToJson(quiz)

        assert j == r"""{"name": "quiz1", "questionNames": ["question1"]}"""

    def test_bigQuiz(self) -> None:
        """Test case for a quiz with multiple questions of different types"""
        question_1 = MultipleChoiceQuestion(
            "question1",
            "Example Question",
            "here's a question",
            ["a", "b", "c"],
            1,
            ["a: wrong", "b: correct", "c: wrong"],
            imgpath="data/questions/yolo.png",
        )

        question_2 = IntegerQuestion(
            "question2",
            "Example Question",
            "here's a question",
            (0, 3),
            ["correct", "too low", "too high"],
        )

        question_3 = WordQuestion(
            "question3",
            "Example Question",
            "here's a question",
            "answer",
            ["correct", "wrong"],
        )

        quiz = Quiz("quiz2", [question_1, question_2, question_3])
        j = QuizSerialiser.quizToJson(quiz)

        assert j == r"""{"name": "quiz2", "questionNames": ["question1","question2","question3"]}"""
