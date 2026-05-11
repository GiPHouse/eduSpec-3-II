import pytest

from managers.QuestionBuilder import QuestionBuilder
from questions.IntegerQuestion import IntegerQuestion
from questions.MoleculeDrawingQuestion import MoleculeDrawingConfig, MoleculeDrawingQuestion
from questions.MultipleChoiceQuestion import MultipleChoiceQuestion
from questions.WordQuestion import WordQuestion

IMAGE_FIGURE_1 = [{"path": "data/img/image1.png", "description": "This is a description"}]


class TestBuildingMCQ:
    """Test cases for building multiple-choice questions"""

    def test_MCQ_1(self) -> None:
        """Test case for building a standard multiple-choice question"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "multipleChoice", "answers": ["a", "b", "c"], "correctAnswer": 1, "feedbacks": ["a: wrong", "b: correct", "c: wrong"]}"""

        correct_mcq = MultipleChoiceQuestion(
            "question1",
            "Example Question",
            "here's a question",
            ["a", "b", "c"],
            1,
            ["a: wrong", "b: correct", "c: wrong"],
            figures=[],
        )

        mcq = QuestionBuilder.questionFromJson(input_data)

        assert isinstance(mcq, MultipleChoiceQuestion)

        assert mcq.name == correct_mcq.name
        assert mcq.title == correct_mcq.title
        assert mcq.bodytext == correct_mcq.bodytext
        assert mcq.figures == correct_mcq.figures
        assert mcq.answers == correct_mcq.answers
        assert mcq.feedbacks == correct_mcq.feedbacks
        assert mcq.correct_answer == correct_mcq.correct_answer

    def test_MCQ_2(self) -> None:
        """Test case for building a standard multiple-choice question with image path"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [{"path": "data/img/image1.png", "description": "This is a description"}], "version": 1, "type": "multipleChoice", "answers": ["a", "b", "c"], "correctAnswer": 1, "feedbacks": ["a: wrong", "b: correct", "c: wrong"]}"""

        correct_mcq = MultipleChoiceQuestion(
            "question1",
            "Example Question",
            "here's a question",
            ["a", "b", "c"],
            1,
            ["a: wrong", "b: correct", "c: wrong"],
            figures=IMAGE_FIGURE_1,
        )

        mcq = QuestionBuilder.questionFromJson(input_data)

        assert isinstance(mcq, MultipleChoiceQuestion)

        assert mcq.name == correct_mcq.name
        assert mcq.title == correct_mcq.title
        assert mcq.bodytext == correct_mcq.bodytext
        assert mcq.figures == correct_mcq.figures
        assert mcq.answers == correct_mcq.answers
        assert mcq.feedbacks == correct_mcq.feedbacks
        assert mcq.correct_answer == correct_mcq.correct_answer

    def test_faulty_MCQ_1(self) -> None:
        """Test case for building a multiple-choice  with a missing id attribute"""
        input_data = r"""{"title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "multipleChoice", "answers": ["a", "b", "c"], "correctAnswer": 1, "feedbacks": ["a: wrong", "b: correct", "c: wrong"]}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), MultipleChoiceQuestion)

    def test_faulty_MCQ_2(self) -> None:
        """Test case for building a multiple-choice question with a missing answers attribute"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "multipleChoice", "correctAnswer": 1, "feedbacks": ["a: wrong", "b: correct", "c: wrong"]}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), MultipleChoiceQuestion)

    def test_faulty_MCQ_3(self) -> None:
        """Test case for building a multiple-choice question with an empty answers attribute"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "multipleChoice", "answers": [], "correctAnswer": 1, "feedbacks": ["a: wrong", "b: correct", "c: wrong"]}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), MultipleChoiceQuestion)

    def test_faulty_MCQ_4(self) -> None:
        """Test case for building a multiple-choice question with a mismatched answers and feedbacks attribute"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "multipleChoice", "answers": ["a", "b"], "correctAnswer": 1, "feedbacks": ["a: wrong", "b: correct", "c: wrong"]}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), MultipleChoiceQuestion)

    def test_faulty_MCQ_5(self) -> None:
        """Test case for building a multiple-choice question with an out-of-index correct answer attribute"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "multipleChoice", "answers": ["a", "b", "c"], "correctAnswer": -1, "feedbacks": ["a: wrong", "b: correct", "c: wrong"]}"""
        input_data_2 = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "multipleChoice", "answers": ["a", "b", "c"], "correctAnswer": 3, "feedbacks": ["a: wrong", "b: correct", "c: wrong"]}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), MultipleChoiceQuestion)

        with pytest.raises(ValueError):
            assert isinstance(
                QuestionBuilder.questionFromJson(input_data_2), MultipleChoiceQuestion
            )


class TestBuildingIntQ:
    """Test cases for building integer questions"""

    def test_IntQ_1(self) -> None:
        """Test case for building a standard integer question"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "integer", "lowerBound": 0, "upperBound": 3, "feedbacks": ["correct", "too low", "too high"]}"""

        correct_intq = IntegerQuestion(
            "question1",
            "Example Question",
            "here's a question",
            (0, 3),
            ["correct", "too low", "too high"],
            figures=[],
        )

        intq = QuestionBuilder.questionFromJson(input_data)

        assert isinstance(intq, IntegerQuestion)

        assert intq.name == correct_intq.name
        assert intq.title == correct_intq.title
        assert intq.bodytext == correct_intq.bodytext
        assert intq.figures == correct_intq.figures
        assert intq.correct_answer == correct_intq.correct_answer
        assert intq.feedbacks == correct_intq.feedbacks

    def test_IntQ_2(self) -> None:
        """Test case for building a standard integer question with image path and equal lower and upper bound"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [{"path": "data/img/image1.png", "description": "This is a description"}], "version": 1, "type": "integer", "lowerBound": 3, "upperBound": 3, "feedbacks": ["correct", "too low", "too high"]}"""

        correct_intq = IntegerQuestion(
            "question1",
            "Example Question",
            "here's a question",
            (3, 3),
            ["correct", "too low", "too high"],
            figures=IMAGE_FIGURE_1,
        )

        intq = QuestionBuilder.questionFromJson(input_data)

        assert isinstance(intq, IntegerQuestion)

        assert intq.name == correct_intq.name
        assert intq.title == correct_intq.title
        assert intq.bodytext == correct_intq.bodytext
        assert intq.figures == correct_intq.figures
        assert intq.correct_answer == correct_intq.correct_answer
        assert intq.feedbacks == correct_intq.feedbacks

    def test_IntQ_3(self) -> None:
        """Test case for building a standard integer question with float bounds"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "integer", "lowerBound": -0.2, "upperBound": 0.3, "feedbacks": ["correct", "too low", "too high"]}"""

        correct_intq = IntegerQuestion(
            "question1",
            "Example Question",
            "here's a question",
            (-0.2, 0.3),
            ["correct", "too low", "too high"],
            figures=[],
        )

        intq = QuestionBuilder.questionFromJson(input_data)

        assert isinstance(intq, IntegerQuestion)

        assert intq.name == correct_intq.name
        assert intq.title == correct_intq.title
        assert intq.bodytext == correct_intq.bodytext
        assert intq.figures == correct_intq.figures
        assert intq.correct_answer == correct_intq.correct_answer
        assert intq.feedbacks == correct_intq.feedbacks

    def test_faulty_IntQ_1(self) -> None:
        """Test case for building an integer question missing the title attribute"""
        input_data = r"""{"id": "question1", "bodyText": "here's a question", "figures": [], "version": 1, "type": "integer", "lowerBound": 0, "upperBound": 3, "feedbacks": ["correct", "too low", "too high"]}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), IntegerQuestion)

    def test_faulty_IntQ_2(self) -> None:
        """Test case for building an integer question missing the lowerBound attribute"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "integer", "upperBound": 3, "feedbacks": ["correct", "too low", "too high"]}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), IntegerQuestion)

    def test_faulty_IntQ_3(self) -> None:
        """Test case for building an integer question with a non-integer upperBound attribute"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "integer", "lowerBound": 0, "upperBound": "a", "feedbacks": ["correct", "too low", "too high"]}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), IntegerQuestion)

    def test_faulty_IntQ_4(self) -> None:
        """Test case for building an integer question with a higher lower bound than upper bound"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "integer", "lowerBound": 6, "upperBound": 3, "feedbacks": ["correct", "too low", "too high"]}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), IntegerQuestion)

    def test_faulty_IntQ_5(self) -> None:
        """Test case for building an integer question with too few feedback options"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "integer", "lowerBound": 0, "upperBound": 3, "feedbacks": ["correct", "too low"]}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), IntegerQuestion)


class TestBuildingWordQ:
    """Test cases for building word questions"""

    def test_WordQ_1(self) -> None:
        """Test case for building a standard integer question"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "word", "correctAnswer": "answer", "correctFeedback": "correct", "incorrectFeedback": "wrong"}"""

        correct_wordq = WordQuestion(
            "question1",
            "Example Question",
            "here's a question",
            "answer",
            ["correct", "wrong"],
            figures=[],
        )

        wordq = QuestionBuilder.questionFromJson(input_data)

        assert isinstance(wordq, WordQuestion)

        assert wordq.name == correct_wordq.name
        assert wordq.title == correct_wordq.title
        assert wordq.bodytext == correct_wordq.bodytext
        assert wordq.figures == correct_wordq.figures
        assert wordq.correct_answer == correct_wordq.correct_answer
        assert wordq.feedbacks == correct_wordq.feedbacks

    def test_WordQ_2(self) -> None:
        """Test case for building a standard word question with image path"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [{"path": "data/img/image1.png", "description": "This is a description"}], "version": 1, "type": "word", "correctAnswer": "answer", "correctFeedback": "correct", "incorrectFeedback": "wrong"}"""

        correct_wordq = WordQuestion(
            "question1",
            "Example Question",
            "here's a question",
            "answer",
            ["correct", "wrong"],
            figures=IMAGE_FIGURE_1,
        )

        wordq = QuestionBuilder.questionFromJson(input_data)

        assert isinstance(wordq, WordQuestion)

        assert wordq.name == correct_wordq.name
        assert wordq.title == correct_wordq.title
        assert wordq.bodytext == correct_wordq.bodytext
        assert wordq.figures == correct_wordq.figures
        assert wordq.correct_answer == correct_wordq.correct_answer
        assert wordq.feedbacks == correct_wordq.feedbacks

    def test_faulty_WordQ_1(self) -> None:
        """Test case for building a word question without figures attribute"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "version": 1, "type": "word", "correctAnswer": "answer", "correctFeedback": "correct", "incorrectFeedback": "wrong"}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), WordQuestion)

    def test_faulty_WordQ_2(self) -> None:
        """Test case for building a word question without correctFeedback attribute"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "word", "correctAnswer": "answer", "incorrectFeedback": "wrong"}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), WordQuestion)

    def test_faulty_WordQ_3(self) -> None:
        """Test case for building a word question with non-string correctAnswer"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "word", "correctAnswer": 3, "correctFeedback": "correct", "incorrectFeedback": "wrong"}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), WordQuestion)

    def test_faulty_WordQ_4(self) -> None:
        """Test case for building a word question with empty correctAnswer"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "word", "correctAnswer": "", "correctFeedback": "correct", "incorrectFeedback": "wrong"}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), WordQuestion)


class TestBuildingDrawingQ:
    """Test cases for building MoleculeDrawingQuestions"""

    def test_WordQ_1(self) -> None:
        """Test case for building a standard drawing question"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "drawing", "correctAnswer": "answer", "defaultAnswer": "seed", "correctFeedback": "correct", "incorrectFeedback": "wrong", "widgetKey": "key"}"""

        correct_drawq = MoleculeDrawingQuestion(
            "question1",
            "Example Question",
            "here's a question",
            MoleculeDrawingConfig("answer", "seed", "key"),
            ["correct", "wrong"],
            figures=[],
        )

        drawq = QuestionBuilder.questionFromJson(input_data)

        assert isinstance(drawq, MoleculeDrawingQuestion)

        assert drawq.name == correct_drawq.name
        assert drawq.title == correct_drawq.title
        assert drawq.bodytext == correct_drawq.bodytext
        assert drawq.figures == correct_drawq.figures
        assert drawq.correct_answer == correct_drawq.correct_answer
        assert drawq.feedbacks == correct_drawq.feedbacks

    def test_WordQ_2(self) -> None:
        """Test case for building a standard word question with image path"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [{"path": "data/img/image1.png", "description": "This is a description"}], "version": 1, "type": "drawing", "correctAnswer": "answer", "defaultAnswer": "", "correctFeedback": "correct", "incorrectFeedback": "wrong", "widgetKey": ""}"""

        correct_drawq = MoleculeDrawingQuestion(
            "question1",
            "Example Question",
            "here's a question",
            MoleculeDrawingConfig("answer", "", ""),
            ["correct", "wrong"],
            figures=IMAGE_FIGURE_1,
        )

        drawq = QuestionBuilder.questionFromJson(input_data)

        assert isinstance(drawq, MoleculeDrawingQuestion)

        assert drawq.name == correct_drawq.name
        assert drawq.title == correct_drawq.title
        assert drawq.bodytext == correct_drawq.bodytext
        assert drawq.figures == correct_drawq.figures
        assert drawq.correct_answer == correct_drawq.correct_answer
        assert drawq.feedbacks == correct_drawq.feedbacks

    def test_faulty_drawQ_1(self) -> None:
        """Test case for building a drawing question without version attribute"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "type": "drawing", "correctAnswer": "answer", "defaultAnswer": "seed", "correctFeedback": "correct", "incorrectFeedback": "wrong", "widgetKey": "key"}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), MoleculeDrawingQuestion)

    def test_faulty_drawQ_2(self) -> None:
        """Test case for building a drawing question without defaultAnswer attribute"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "drawing", "correctAnswer": "answer", "correctFeedback": "correct", "incorrectFeedback": "wrong", "widgetKey": "key"}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), MoleculeDrawingQuestion)

    def test_faulty_drawQ_3(self) -> None:
        """Test case for building a drawing question with non-string widgetKey"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "drawing", "correctAnswer": "answer", "defaultAnswer": "seed", "correctFeedback": "correct", "incorrectFeedback": "wrong", "widgetKey": 0.3}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), MoleculeDrawingQuestion)

    def test_faulty_drawQ_4(self) -> None:
        """Test case for building a drawing question with empty incorrectFeedback"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "figures": [], "version": 1, "type": "drawing", "correctAnswer": "answer", "defaultAnswer": "seed", "correctFeedback": "correct", "incorrectFeedback": "", "widgetKey": "key"}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), MoleculeDrawingQuestion)
