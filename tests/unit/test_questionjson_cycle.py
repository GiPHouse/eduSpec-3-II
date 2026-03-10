from managers.QuestionBuilder import QuestionBuilder
from managers.QuestionSerialiser import QuestionSerialiser
from questions.IntegerQuestion import IntegerQuestion
from questions.MultipleChoiceQuestion import MultipleChoiceQuestion
from questions.WordQuestion import WordQuestion


class TestSerialisationCycle:
    """Test cases for the serialisation and de-serialisation consistency of all question types"""

    def test_MCQ(self) -> None:
        """Test case for a serialisation cycle of multiple-choice questions"""
        mcq_1 = MultipleChoiceQuestion(
            "question1",
            "Example Question",
            "here's a question",
            ["a", "b", "c"],
            1,
            ["a: wrong", "b: correct", "c: wrong"],
            imgpath="data/img/image1.png",
        )
        json_1 = QuestionSerialiser.questionToJson(mcq_1)

        mcq_2 = QuestionBuilder.questionFromJson(json_1)

        json_2 = QuestionSerialiser.questionToJson(mcq_2)

        assert json_1 == json_2

    def test_IntQ(self) -> None:
        """Test case for a serialisation cycle of integer questions"""
        intq_1 = IntegerQuestion(
            "question2",
            "Example Question",
            "here's a question",
            (0, 3),
            ["correct", "too low", "too high"],
            imgpath="data/img/image2.png",
        )
        json_1 = QuestionSerialiser.questionToJson(intq_1)

        intq_2 = QuestionBuilder.questionFromJson(json_1)

        json_2 = QuestionSerialiser.questionToJson(intq_2)

        assert json_1 == json_2

    def test_WordQ(self) -> None:
        """Test case for a serialisation cycle of word questions"""
        wordq_1 = WordQuestion(
            "question3",
            "Example Question",
            "here's a question",
            "The correct answer",
            ["correct", "wrong"],
            imgpath="data/img/image1.png",
        )
        json_1 = QuestionSerialiser.questionToJson(wordq_1)

        wordq_2 = QuestionBuilder.questionFromJson(json_1)

        json_2 = QuestionSerialiser.questionToJson(wordq_2)

        assert json_1 == json_2
