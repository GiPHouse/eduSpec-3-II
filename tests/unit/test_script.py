from typing import Any
from unittest.mock import patch

import pytest

from Script import Script


def test_get_file_name_returns_original_name() -> None:
    """Test that Script stores and returns the script filename."""
    script = Script("example_script.py")

    assert script.get_file_name() == "example_script.py"


def test_run_imports_and_calls_script_run_function() -> None:
    """Test that run imports the script function and passes params to it."""
    params = {"x": 3}
    expected = {"correct": True, "feedback": "ok"}

    def fake_run(received_params: dict[str, Any]) -> dict[str, Any]:
        assert received_params == params
        return expected

    with patch(
        "managers.ScriptManager.ScriptManager.importRunFunction",
        return_value=fake_run,
    ) as import_mock:
        script = Script("example_script.py")
        result = script.run(params)

    import_mock.assert_called_once_with("example_script.py")
    assert result == expected


def test_run_rejects_non_dictionary_result() -> None:
    """Test that run raises TypeError when script output is not a dictionary."""

    def fake_run(params: dict[str, Any]) -> list[str]:
        return ["not", "a", "dict"]

    with patch(
        "managers.ScriptManager.ScriptManager.importRunFunction",
        return_value=fake_run,
    ):
        script = Script("bad_script.py")

        with pytest.raises(TypeError, match="must return a dictionary"):
            script.run({"x": 1})
