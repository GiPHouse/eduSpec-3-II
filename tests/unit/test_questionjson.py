import json

from managers.QuestionSerialiser import QuestionSerialiser
from questions.IntegerQuestion import IntegerQuestion
from questions.MoleculeDrawingQuestion import MoleculeDrawingConfig, MoleculeDrawingQuestion
from questions.MultipleChoiceQuestion import MultipleChoiceQuestion
from questions.WordQuestion import WordQuestion


class TestSerialisationMCQ:
    """Test cases for the serialisation of multiple-choice questions."""

    def test_MCQ(self) -> None:
        """Test case for standard multiple-choice question serialisation."""
        mcq = MultipleChoiceQuestion(
            name="question1",
            title="Example Question",
            bodytext="here's a question",
            answers=["a", "b", "c"],
            correct_answer=1,
            feedbacks=["a: wrong", "b: correct", "c: wrong"],
            body_format="text",
        )

        j = json.loads(QuestionSerialiser.questionToJson(mcq))

        assert j == {
            "id": "question1",
            "title": "Example Question",
            "bodyText": "here's a question",
            "bodyFormat": "text",
            "figures": [],
            "version": 1,
            "type": "multipleChoice",
            "answers": ["a", "b", "c"],
            "correctAnswer": 1,
            "feedbacks": ["a: wrong", "b: correct", "c: wrong"],
        }

    def test_MCQfigures(self) -> None:
        """Test case for multiple choice question serialisation with an image path."""
        mcq = MultipleChoiceQuestion(
            name="question1",
            title="Example Question",
            bodytext="here's a question",
            answers=["a", "b", "c"],
            correct_answer=1,
            feedbacks=["a: wrong", "b: correct", "c: wrong"],
            figures=["data/img/image1.png"],
            body_format="text",
        )

        j = json.loads(QuestionSerialiser.questionToJson(mcq))

        assert j == {
            "id": "question1",
            "title": "Example Question",
            "bodyText": "here's a question",
            "bodyFormat": "text",
            "figures": ["data/img/image1.png"],
            "version": 1,
            "type": "multipleChoice",
            "answers": ["a", "b", "c"],
            "correctAnswer": 1,
            "feedbacks": ["a: wrong", "b: correct", "c: wrong"],
        }


class TestSerialisationIntQ:
    """Test cases for the serialisation of integer questions."""

    def test_IntQ(self) -> None:
        """Test case for standard integer question serialisation."""
        intq = IntegerQuestion(
            name="question1",
            title="Example Question",
            bodytext="here's a question",
            correct_answer=(0, 3),
            feedbacks=["correct", "too low", "too high"],
            body_format="text",
        )

        j = json.loads(QuestionSerialiser.questionToJson(intq))

        assert j == {
            "id": "question1",
            "title": "Example Question",
            "bodyText": "here's a question",
            "bodyFormat": "text",
            "figures": [],
            "version": 1,
            "type": "integer",
            "lowerBound": 0,
            "upperBound": 3,
            "feedbacks": ["correct", "too low", "too high"],
        }


class TestSerialisationWordQ:
    """Test cases for the serialisation of word questions."""

    def test_WordQ(self) -> None:
        """Test case for standard word question serialisation."""
        wordq = WordQuestion(
            name="question1",
            title="Example Question",
            bodytext="here's a question",
            correct_answer="answer",
            feedbacks=["correct", "wrong"],
            body_format="text",
        )

        j = json.loads(QuestionSerialiser.questionToJson(wordq))

        assert j == {
            "id": "question1",
            "title": "Example Question",
            "bodyText": "here's a question",
            "bodyFormat": "text",
            "figures": [],
            "version": 1,
            "type": "word",
            "correctAnswer": "answer",
            "correctFeedback": "correct",
            "incorrectFeedback": "wrong",
        }


class TestSerialisationDrawQ:
    """Test cases for the serialisation of drawing questions."""

    def test_DrawQ(self) -> None:
        """Test case for standard drawing question serialisation."""
        drawq = MoleculeDrawingQuestion(
            name="question1",
            title="Example Question",
            bodytext="here's a question",
            config=MoleculeDrawingConfig("answer", "seed", "key"),
            feedbacks=["correct", "wrong"],
            body_format="text",
        )

        j = json.loads(QuestionSerialiser.questionToJson(drawq))

        assert j == {
            "id": "question1",
            "title": "Example Question",
            "bodyText": "here's a question",
            "bodyFormat": "text",
            "figures": [],
            "version": 1,
            "type": "drawing",
            "correctAnswer": "answer",
            "defaultAnswer": "seed",
            "correctFeedback": "correct",
            "incorrectFeedback": "wrong",
            "widgetKey": "key",
        }
