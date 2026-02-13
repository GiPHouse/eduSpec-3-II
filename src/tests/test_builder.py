import pytest

from MultipleChoiceQuestion import MultipleChoiceQuestion
from QuestionBuilder import QuestionBuilder


class TestBuildingMCQ:
    """Test cases for building multiple choice questions"""

    def test_MCQ(self) -> None:
        """Test case for building a standard multiple choice question"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "imagePath": "", "version": 1, "type": "multipleChoice", "answers": ["a", "b", "c"], "correctAnswer": 1, "feedbacks": ["a: wrong", "b: correct", "c: wrong"]}"""

        correct_mcq = MultipleChoiceQuestion(
            "question1",
            "Example Question",
            "here's a question",
            ["a", "b", "c"],
            1,
            ["a: wrong", "b: correct", "c: wrong"],
            None,
        )

        mcq = QuestionBuilder.questionFromJson(input_data)

        assert isinstance(mcq, MultipleChoiceQuestion)

        assert mcq.name == correct_mcq.name
        assert mcq.title == correct_mcq.title
        assert mcq.bodytext == correct_mcq.bodytext
        assert mcq.imgpath == correct_mcq.imgpath
        assert mcq.answers == correct_mcq.answers
        assert mcq.feedbacks == correct_mcq.feedbacks
        assert mcq.correct_answer == correct_mcq.correct_answer

    def test_faulty_MCQ_1(self) -> None:
        """Test case for building a multiple choice  with a missing id attribute"""
        input_data = r"""{"title": "Example Question", "bodyText": "here's a question", "imagePath": "", "version": 1, "type": "multipleChoice", "answers": ["a", "b", "c"], "correctAnswer": 1, "feedbacks": ["a: wrong", "b: correct", "c: wrong"]}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), MultipleChoiceQuestion)

    def test_faulty_MCQ_2(self) -> None:
        """Test case for building a multiple choice question with a missing answers attribute"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "imagePath": "", "version": 1, "type": "multipleChoice", "correctAnswer": 1, "feedbacks": ["a: wrong", "b: correct", "c: wrong"]}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), MultipleChoiceQuestion)

    def test_faulty_MCQ_3(self) -> None:
        """Test case for building a multiple choice question with an empty answers attribute"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "imagePath": "", "version": 1, "type": "multipleChoice", "answers": [], "correctAnswer": 1, "feedbacks": ["a: wrong", "b: correct", "c: wrong"]}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), MultipleChoiceQuestion)

    def test_faulty_MCQ_4(self) -> None:
        """Test case for building a multiple choice question with a mismatched answers and feedbacks attribute"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "imagePath": "", "version": 1, "type": "multipleChoice", "answers": ["a", "b"], "correctAnswer": 1, "feedbacks": ["a: wrong", "b: correct", "c: wrong"]}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), MultipleChoiceQuestion)

    def test_faulty_MCQ_5(self) -> None:
        """Test case for building a multiple choice question with an out-of-index correct answer attribute"""
        input_data = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "imagePath": "", "version": 1, "type": "multipleChoice", "answers": ["a", "b", "c"], "correctAnswer": -1, "feedbacks": ["a: wrong", "b: correct", "c: wrong"]}"""
        input_data_2 = r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "imagePath": "", "version": 1, "type": "multipleChoice", "answers": ["a", "b", "c"], "correctAnswer": 3, "feedbacks": ["a: wrong", "b: correct", "c: wrong"]}"""

        with pytest.raises(ValueError):
            assert isinstance(QuestionBuilder.questionFromJson(input_data), MultipleChoiceQuestion)

        with pytest.raises(ValueError):
            assert isinstance(
                QuestionBuilder.questionFromJson(input_data_2), MultipleChoiceQuestion
            )
