import pytest

from questions.SpectralQuestion import SpectralQuestion, SpectralType


@pytest.fixture
def sq() -> SpectralQuestion:
    """Create a SpectralQuestion fixture."""
    return SpectralQuestion(
        name="question5",
        title="title5",
        bodytext="this is a bodytext",
        body_format="text",
        correct_answer=1000.00,
        feedbacks=["correct", "wrong"],
        figures=["data/images/test.png"],
        spectralpath="data/spectra/easy001/ms.dx",
        tolerance=50,
    )


class TestSpectralQuestionExtra:
    """Test class for word question"""

    def test_init_sets_attributes(self, sq: SpectralQuestion) -> None:
        """Test that init sets the basic attributes."""
        assert sq.name == "question5"
        assert sq.title == "title5"
        assert sq.bodytext == "this is a bodytext"
        assert sq.correct_answer == 1000.00
        assert sq.feedbacks == ["correct", "wrong"]
        assert sq.spectralpath == "data/spectra/easy001/ms.dx"
        assert sq.type == SpectralType.MS

    def test_init_sets_widget_key(self, sq: SpectralQuestion) -> None:
        """Test that init sets the widget key."""
        assert sq.widget_key == f"spectral_question_{sq.name}"

    def test_init_sets_default_empty_string(self, sq: SpectralQuestion) -> None:
        """Test that init sets the default value."""
        assert sq.default is None

    def test_verify_exact_match_required(self, sq: SpectralQuestion) -> None:
        """Test that answers must match exactly."""
        assert sq.verifyAndFeedback(1050) == (True, "correct")
        assert sq.verifyAndFeedback(1051) == (False, "wrong")

        assert sq.verifyAndFeedback(949) == (False, "wrong")
        assert sq.verifyAndFeedback(950) == (True, "correct")

    def test_verify_none_string_is_incorrect(self, sq: SpectralQuestion) -> None:
        """Test that an empty string is incorrect."""
        with pytest.raises(
            TypeError,
            match="You wanted to check if a user input is the correct answer, but you didn't provide the user input itself!",
        ):
            sq.verifyAndFeedback(None)

    def test_verify_empty_string_is_incorrect(self, sq: SpectralQuestion) -> None:
        """Test that an empty string is incorrect."""
        with pytest.raises(TypeError):
            sq.verifyAndFeedback()

    def test_verify_whitespace_only_is_incorrect(self, sq: SpectralQuestion) -> None:
        """Test that whitespace-only input is incorrect."""
        with pytest.raises(TypeError):
            sq.verifyAndFeedback("")

    def test_verify_with_different_correct_answer(self) -> None:
        """Test verification with a different correct answer."""
        question = SpectralQuestion(
            name="question5",
            title="title5",
            bodytext="this is a bodytext",
            body_format="text",
            correct_answer=0.00,
            feedbacks=["correct", "wrong"],
            figures=["data/images/test.png"],
            spectralpath="data/spectra/easy001/ms.dx",
            tolerance=50,
        )

        assert question.verifyAndFeedback(0) == (True, "correct")
        assert question.verifyAndFeedback(1000) == (False, "wrong")

    # Some tests we have for wordquestion are irrelevant for spectral, so I deleted them.
