from MultipleChoiceQuestion import MultipleChoiceQuestion
from QuestionSerialiser import QuestionSerialiser


class TestSerialisationMCQ:
    """Test cases for the serialisation of multiple choice questions"""

    def test_MCQ(self) -> None:
        """Test case for standard multiple choice question serialisation"""
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
            == r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "imagePath": "", "version": 1, "type": "multipleChoice", "answers": ["a", "b", "c"], "correctAnswer": 1, "feedbacks": ["a: wrong", "b: correct", "c: wrong"]}"""
        )

    def test_MCQImgPath(self) -> None:
        """Test case for multiple choice question serialisation with an image path"""
        mcq = MultipleChoiceQuestion(
            "question1",
            "Example Question",
            "here's a question",
            ["a", "b", "c"],
            1,
            ["a: wrong", "b: correct", "c: wrong"],
            imgpath="data/img/image1.png",
        )
        j = QuestionSerialiser.questionToJson(mcq)

        assert (
            j
            == r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "imagePath": "data/img/image1.png", "version": 1, "type": "multipleChoice", "answers": ["a", "b", "c"], "correctAnswer": 1, "feedbacks": ["a: wrong", "b: correct", "c: wrong"]}"""
        )
