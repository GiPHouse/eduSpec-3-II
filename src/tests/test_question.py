import pytest

from ..Question import Question


def test_createQuestion() -> None:
    """Test case for the base question.

    Creating a base Question instance should fail with a TypeError
    """
    with pytest.raises(TypeError):
        question = Question("a", "b")  # noqa: F841
