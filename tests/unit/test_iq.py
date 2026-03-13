from questions.IntegerQuestion import IntegerQuestion


class TestIQ:
    """Tests for the model of integer questions"""

    def test_correct_answers_are_valid(self) -> None:
        """Test case to check if the range of correct answers is valid"""
        iq = IntegerQuestion(
            "question1",
            "Example Question",
            "here's a question",
            (10, 12.5),
            ["correct", "wrong, too small", "wrong, too big"],
        )

        assert iq.verifyAndFeedback(0) == (False, "wrong, too small")
        assert iq.verifyAndFeedback(11) == (True, "correct")
        assert iq.verifyAndFeedback(20) == (False, "wrong, too big")

    def test_negative_numbers(self) -> None:
        """Test case for answers that are negative"""
        iq = IntegerQuestion(
            "question1",
            "Example Question",
            "here's a question",
            (-10, -3),
            ["correct", "wrong, too small", "wrong, too big"],
        )

        assert iq.verifyAndFeedback(-100) == (False, "wrong, too small")
        assert iq.verifyAndFeedback(-5) == (True, "correct")
        assert iq.verifyAndFeedback(20) == (False, "wrong, too big")
