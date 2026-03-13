import pytest
from IntegerQuestion import IntegerQuestion

# Still needs streamlit tests...


@pytest.fixture
def iq() -> IntegerQuestion:
    """Fixture for creating a IntegerQuestion instance for testing

    Returns:
        IntegerQuestion: the question
    """
    return IntegerQuestion(
        name="question1",
        title="exampleQuestion",
        bodytext="this is the body text of the question",
        correct_answer=(10, 20),
        feedbacks=["correct", "wrong, too small", "wrong, too big"],
    )


class TestIQ:
    """Tests for the model of integer questions"""

    def test_correct_input(self, iq: IntegerQuestion) -> None:
        """Test case to check if the range of correct answers is valid"""
        assert iq.verifyAndFeedback(-100) == (False, "wrong, too small")
        assert iq.verifyAndFeedback(12) == (True, "correct")
        assert iq.verifyAndFeedback(21) == (False, "wrong, too big")

    def test_wrong_input(self, iq: IntegerQuestion) -> None:
        """Test for type errors

        Args:
            iq (IntegerQuestion): the question
        """
        with pytest.raises(TypeError):
            assert iq.verifyAndFeedback("aa") == (False, "")

        with pytest.raises(TypeError):
            assert iq.verifyAndFeedback(["test"]) == (False, "")
