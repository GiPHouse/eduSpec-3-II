import pytest

from questions.WordQuestion import WordQuestion


@pytest.fixture
def wq() -> WordQuestion:
    """Create a WordQuestion fixture."""
    return WordQuestion(
        name="question1",
        title="Example Question",
        bodytext="here's a question",
        correct_answer="correct answer",
        feedbacks=["correct", "incorrect"],
    )


class TestWordQuestionExtra:
    """Test class for word question"""

    def test_init_sets_attributes(self, wq: WordQuestion) -> None:
        """Test that init sets the basic attributes."""
        assert wq.name == "question1"
        assert wq.title == "Example Question"
        assert wq.bodytext == "here's a question"
        assert wq.correct_answer == "correct answer"
        assert wq.feedbacks == ["correct", "incorrect"]

    def test_init_sets_widget_key(self, wq: WordQuestion) -> None:
        """Test that init sets the widget key."""
        assert wq.widget_key == "word_input_Example Question"

    def test_init_sets_default_empty_string(self, wq: WordQuestion) -> None:
        """Test that init sets the default value."""
        assert wq.default == ""

    def test_feedback_returns_none(self, wq: WordQuestion) -> None:
        """Test that feedback returns None."""
        assert wq.feedback() is None

    def test_verify_exact_match_required(self, wq: WordQuestion) -> None:
        """Test that answers must match exactly."""
        assert wq.verifyAndFeedback("correct answer") == (True, "correct")
        assert wq.verifyAndFeedback("correct answer ") == (False, "incorrect")
        assert wq.verifyAndFeedback(" correct answer") == (False, "incorrect")

    def test_verify_is_case_sensitive(self, wq: WordQuestion) -> None:
        """Test that answer checking is case sensitive."""
        assert wq.verifyAndFeedback("Correct answer") == (False, "incorrect")
        assert wq.verifyAndFeedback("CORRECT ANSWER") == (False, "incorrect")

    def test_verify_empty_string_is_incorrect(self, wq: WordQuestion) -> None:
        """Test that an empty string is incorrect."""
        assert wq.verifyAndFeedback("") == (False, "incorrect")

    def test_verify_whitespace_only_is_incorrect(self, wq: WordQuestion) -> None:
        """Test that whitespace-only input is incorrect."""
        assert wq.verifyAndFeedback("   ") == (False, "incorrect")

    def test_verify_special_characters_do_not_match(self, wq: WordQuestion) -> None:
        """Test that special-character variants do not match."""
        assert wq.verifyAndFeedback("correct-answer") == (False, "incorrect")
        assert wq.verifyAndFeedback("correct_answer") == (False, "incorrect")

    def test_verify_with_different_correct_answer(self) -> None:
        """Test verification with a different correct answer."""
        question = WordQuestion(
            name="question2",
            title="Math Question",
            bodytext="What is 2+2?",
            correct_answer="4",
            feedbacks=["yes", "no"],
        )

        assert question.verifyAndFeedback("4") == (True, "yes")
        assert question.verifyAndFeedback("four") == (False, "no")

    @pytest.mark.parametrize(
        ("user_input", "expected"),
        [
            ("correct answer", (True, "correct")),
            ("wrong", (False, "incorrect")),
            ("", (False, "incorrect")),
            (" ", (False, "incorrect")),
            ("Correct answer", (False, "incorrect")),
            ("correct answer ", (False, "incorrect")),
        ],
    )
    def test_verify_multiple_inputs(
        self,
        wq: WordQuestion,
        user_input: str,
        expected: tuple[bool, str],
    ) -> None:
        """Test multiple input variants."""
        assert wq.verifyAndFeedback(user_input) == expected
