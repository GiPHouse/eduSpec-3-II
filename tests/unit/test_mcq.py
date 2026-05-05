import pytest

from questions.MultipleChoiceQuestion import MultipleChoiceQuestion


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

        # Case of python being fucked up. Index -1 is the last entry.
        assert mcq.verifyAndFeedback(-1) == mcq.verifyAndFeedback(2)

        with pytest.raises(IndexError):
            assert mcq.verifyAndFeedback(3) == (False, "")

        with pytest.raises(TypeError):
            assert mcq.verifyAndFeedback(1.5) == (False, "")  # type: ignore


@pytest.fixture
def mcq() -> MultipleChoiceQuestion:
    """Create a MultipleChoiceQuestion fixture."""
    return MultipleChoiceQuestion(
        "question1",
        "Example Question",
        "here's a question",
        ["a", "b", "c"],
        1,
        ["a: wrong", "b: correct", "c: wrong"],
    )


class TestMCQExtra:
    """Extra unit tests for multiple choice questions."""

    def test_init_sets_attributes(self, mcq: MultipleChoiceQuestion) -> None:
        """Test that init sets the basic attributes."""
        assert mcq.name == "question1"
        assert mcq.title == "Example Question"
        assert mcq.bodytext == "here's a question"
        assert mcq.answers == ["a", "b", "c"]
        assert mcq.correct_answer == 1
        assert mcq.feedbacks == ["a: wrong", "b: correct", "c: wrong"]

    def test_init_sets_widget_key(self, mcq: MultipleChoiceQuestion) -> None:
        """Test that init sets the widget key."""
        assert mcq.widget_key == "multiple_choice_Example Question"

    def test_init_sets_default_none(self, mcq: MultipleChoiceQuestion) -> None:
        """Test that init sets the default value."""
        assert mcq.default is None

    def test_feedback_returns_expected_entry(self, mcq: MultipleChoiceQuestion) -> None:
        """Test that feedback returns the matching feedback entry."""
        assert mcq.feedback(0) == "a: wrong"
        assert mcq.feedback(1) == "b: correct"
        assert mcq.feedback(2) == "c: wrong"

    def test_verify_correct_answer(self, mcq: MultipleChoiceQuestion) -> None:
        """Test that the correct answer is marked correct."""
        assert mcq.verifyAndFeedback(1) == (True, "b: correct")

    def test_verify_incorrect_answers(self, mcq: MultipleChoiceQuestion) -> None:
        """Test that incorrect answers are marked incorrect."""
        assert mcq.verifyAndFeedback(0) == (False, "a: wrong")
        assert mcq.verifyAndFeedback(2) == (False, "c: wrong")

    def test_invalid_feedback_length_raises_assertion(self) -> None:
        """Test that mismatched answers and feedback lengths raise an assertion."""
        with pytest.raises(AssertionError):
            MultipleChoiceQuestion(
                "question1",
                "Example Question",
                "here's a question",
                ["a", "b", "c"],
                1,
                ["wrong", "correct"],
            )

    def test_negative_correct_answer_raises_assertion(self) -> None:
        """Test that a negative correct answer index raises an assertion."""
        with pytest.raises(AssertionError):
            MultipleChoiceQuestion(
                "question1",
                "Example Question",
                "here's a question",
                ["a", "b", "c"],
                -1,
                ["a: wrong", "b: correct", "c: wrong"],
            )

    def test_too_large_correct_answer_raises_assertion(self) -> None:
        """Test that an out-of-range correct answer index raises an assertion."""
        with pytest.raises(AssertionError):
            MultipleChoiceQuestion(
                "question1",
                "Example Question",
                "here's a question",
                ["a", "b", "c"],
                3,
                ["a: wrong", "b: correct", "c: wrong"],
            )
