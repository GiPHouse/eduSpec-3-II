from collections.abc import Callable
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType

from managers.BaseManager import BaseManager
from Script import Script


class ScriptManager(BaseManager):
    """Manager for custom interactive scripts."""

    _item_dir = Path("scripts/")

    @classmethod
    def buildScript(cls, name: str) -> Script:
        """Build a serializable Script object from a script file name."""
        # Validate once when the question is loaded.
        cls.importRunFunction(name)

        # Store only the script name, not the imported function.
        return Script(name)

    @classmethod
    def importRunFunction(cls, name: str) -> Callable:
        """Import the run function from a script file.

        The script must define:

            def run(params: dict) -> dict:
                ...
        """
        script_dir = cls._getDir()
        file_name = name if name.endswith(".py") else f"{name}.py"
        script_path = script_dir / file_name

        if not script_path.is_file():
            raise FileNotFoundError(f"Script {file_name} does not exist in {script_dir}")

        module_name = f"custom_script_{script_path.stem}"
        spec = spec_from_file_location(module_name, script_path)

        if spec is None or spec.loader is None:
            raise ImportError(f"Could not import script {file_name}")

        module = module_from_spec(spec)
        spec.loader.exec_module(module)

        if not cls._validateScript(module):
            raise NameError("No valid function `run(params) -> dict` found")

        return module.run

    @classmethod
    def _validateScript(cls, script_file: ModuleType) -> bool:
        """Check whether the script file contains a callable run function."""
        run_function = getattr(script_file, "run", None)
        return isinstance(run_function, Callable)
