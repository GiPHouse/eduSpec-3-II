import pytest

from questions.WordQuestion import WordQuestion


@pytest.fixture
def wq() -> WordQuestion:
    """Fixture for creating a WordQuestion instance for testing"""
    return WordQuestion(
        name="question1",
        title="Example Question",
        bodytext="here's a question",
        correct_answer="correct answer",
        feedbacks=["correct", "incorrect"],
    )


class TestWordQuestion:
    """Tests for the model of word questions"""

    def test_verify_correct(self, wq: WordQuestion) -> None:
        """Test case for correct answer"""
        assert wq.verifyAndFeedback("correct answer") == (True, "correct")

    def test_verify_incorrect(self, wq: WordQuestion) -> None:
        """Test case for incorrect answer"""
        assert wq.verifyAndFeedback("wrong") == (False, "incorrect")

    @pytest.mark.parametrize(
        ("user_input", "expected"),
        [
            ("correct answer", (True, "correct")),
            ("wrong", (False, "incorrect")),
        ],
    )
    def test_verify_variants(
        self,
        wq: WordQuestion,
        user_input: str,
        expected: tuple[bool, str],
    ) -> None:
        """Test case for multiple variants of user input"""
        assert wq.verifyAndFeedback(user_input) == expected
