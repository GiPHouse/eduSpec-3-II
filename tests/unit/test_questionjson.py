from managers.QuestionSerialiser import QuestionSerialiser
from questions.IntegerQuestion import IntegerQuestion
from questions.MoleculeDrawingQuestion import MoleculeDrawingConfig, MoleculeDrawingQuestion
from questions.MultipleChoiceQuestion import MultipleChoiceQuestion
from questions.WordQuestion import WordQuestion


class TestSerialisationMCQ:
    """Test cases for the serialisation of multiple-choice questions"""

    def test_MCQ(self) -> None:
        """Test case for standard multiple-choice question serialisation"""
        mcq = MultipleChoiceQuestion(
            "question1",
            "Example Question",
            "here's a question",
            ["a", "b", "c"],
            1,
            ["a: wrong", "b: correct", "c: wrong"],
        )
        j = QuestionSerialiser.questionToJson(mcq)

        assert (
            j
            == r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "multipleChoice", "answers": ["a", "b", "c"], "correctAnswer": 1, "feedbacks": ["a: wrong", "b: correct", "c: wrong"]}"""
        )

    def test_MCQfigures(self) -> None:
        """Test case for multiple choice question serialisation with an image path"""
        mcq = MultipleChoiceQuestion(
            "question1",
            "Example Question",
            "here's a question",
            ["a", "b", "c"],
            1,
            ["a: wrong", "b: correct", "c: wrong"],
            figures=["data/img/image1.png"],
        )
        j = QuestionSerialiser.questionToJson(mcq)

        assert (
            j
            == r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": ["data/img/image1.png"], "version": 1, "type": "multipleChoice", "answers": ["a", "b", "c"], "correctAnswer": 1, "feedbacks": ["a: wrong", "b: correct", "c: wrong"]}"""
        )


class TestSerialisationIntQ:
    """Test cases for the serialisation of integer questions"""

    def test_IntQ(self) -> None:
        """Test case for standard integer question serialisation"""
        intq = IntegerQuestion(
            "question1",
            "Example Question",
            "here's a question",
            (0, 3),
            ["correct", "too low", "too high"],
        )
        j = QuestionSerialiser.questionToJson(intq)

        assert (
            j
            == r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "integer", "lowerBound": 0, "upperBound": 3, "feedbacks": ["correct", "too low", "too high"]}"""
        )


class TestSerialisationWordQ:
    """Test cases for the serialisation of word questions"""

    def test_WordQ(self) -> None:
        """Test case for standard word question serialisation"""
        wordq = WordQuestion(
            "question1",
            "Example Question",
            "here's a question",
            "answer",
            ["correct", "wrong"],
        )
        j = QuestionSerialiser.questionToJson(wordq)

        assert (
            j
            == r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "word", "correctAnswer": "answer", "correctFeedback": "correct", "incorrectFeedback": "wrong"}"""
        )


class TestSerialisationDrawQ:
    """Test cases for the serialisation of drawing questions"""

    def test_DrawQ(self) -> None:
        """Test case for standard drawing question serialisation"""
        drawq = MoleculeDrawingQuestion(
            "question1",
            "Example Question",
            "here's a question",
            MoleculeDrawingConfig("answer", "seed", "key"),
            ["correct", "wrong"],
        )
        j = QuestionSerialiser.questionToJson(drawq)

        assert (
            j
            == r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "drawing", "correctAnswer": "answer", "defaultAnswer": "seed", "correctFeedback": "correct", "incorrectFeedback": "wrong", "widgetKey": "key"}"""
        )
