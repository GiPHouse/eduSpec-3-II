from pathlib import Path
from unittest.mock import patch

import pytest

from managers.ScriptManager import ScriptManager
from Script import Script


def test_import_run_function_imports_valid_script(tmp_path: Path) -> None:
    """Test that a valid script file returns its run function."""
    script_file = tmp_path / "valid_script.py"
    script_file.write_text(
        "def run(params: dict) -> dict:\n"
        "    return {'correct': params['answer'] == 4, 'feedback': 'done'}\n",
        encoding="utf-8",
    )

    with patch.object(ScriptManager, "_getDir", return_value=tmp_path):
        run_function = ScriptManager.importRunFunction("valid_script")

    assert run_function({"answer": 4}) == {"correct": True, "feedback": "done"}
    assert run_function({"answer": 3}) == {"correct": False, "feedback": "done"}


def test_import_run_function_accepts_name_with_py_extension(tmp_path: Path) -> None:
    """Test that script names ending in .py are accepted."""
    script_file = tmp_path / "valid_script.py"
    script_file.write_text(
        "def run(params: dict) -> dict:\n    return {'correct': True, 'feedback': 'ok'}\n",
        encoding="utf-8",
    )

    with patch.object(ScriptManager, "_getDir", return_value=tmp_path):
        run_function = ScriptManager.importRunFunction("valid_script.py")

    assert run_function({}) == {"correct": True, "feedback": "ok"}


def test_import_run_function_raises_for_missing_script(tmp_path: Path) -> None:
    """Test that a missing script file raises FileNotFoundError."""
    with patch.object(ScriptManager, "_getDir", return_value=tmp_path):
        with pytest.raises(FileNotFoundError, match="does not exist"):
            ScriptManager.importRunFunction("missing_script")


def test_import_run_function_raises_when_run_is_missing(tmp_path: Path) -> None:
    """Test that a script without a run function raises NameError."""
    script_file = tmp_path / "invalid_script.py"
    script_file.write_text("VALUE = 10\n", encoding="utf-8")

    with patch.object(ScriptManager, "_getDir", return_value=tmp_path):
        with pytest.raises(NameError, match="No valid function"):
            ScriptManager.importRunFunction("invalid_script")


def test_import_run_function_raises_when_run_is_not_callable(tmp_path: Path) -> None:
    """Test that a non-callable run attribute raises NameError."""
    script_file = tmp_path / "invalid_script.py"
    script_file.write_text("run = 'not callable'\n", encoding="utf-8")

    with patch.object(ScriptManager, "_getDir", return_value=tmp_path):
        with pytest.raises(NameError, match="No valid function"):
            ScriptManager.importRunFunction("invalid_script")


def test_build_script_validates_and_returns_script_object(tmp_path: Path) -> None:
    """Test that buildScript validates the file and returns a Script object."""
    script_file = tmp_path / "valid_script.py"
    script_file.write_text(
        "def run(params: dict) -> dict:\n    return {'correct': True, 'feedback': 'ok'}\n",
        encoding="utf-8",
    )

    with patch.object(ScriptManager, "_getDir", return_value=tmp_path):
        script = ScriptManager.buildScript("valid_script.py")

    assert isinstance(script, Script)
    assert script.get_file_name() == "valid_script.py"
