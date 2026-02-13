import pytest

from MultipleChoiceQuestion import MultipleChoiceQuestion


class TestMCQ:
    """Tests for the model of multiple choice questions"""

    def test_answers_3(self) -> None:
        """Test case for 3 different answers"""
        mcq = MultipleChoiceQuestion(
            "question1",
            "Example Question",
            "here's a question",
            ["a", "b", "c"],
            1,
            ["a: wrong", "b: correct", "c: wrong"],
        )

        assert mcq.verifyAndFeedback(0) == (False, "a: wrong")
        assert mcq.verifyAndFeedback(1) == (True, "b: correct")
        assert mcq.verifyAndFeedback(2) == (False, "c: wrong")

    def test_answers_outside_range(self) -> None:
        """Test case for answers that are outside the range"""
        mcq = MultipleChoiceQuestion(
            "question1",
            "Example Question",
            "here's a question",
            ["a", "b", "c"],
            1,
            ["a: wrong", "b: wrong", "c: wrong"],
        )

        # Case of python being fucked up
        assert mcq.verifyAndFeedback(-1) == mcq.verifyAndFeedback(2)

        with pytest.raises(IndexError):
            assert mcq.verifyAndFeedback(3) == (False, "")

        with pytest.raises(TypeError):
            assert mcq.verifyAndFeedback(1.5) == (False, "")  # type: ignore
