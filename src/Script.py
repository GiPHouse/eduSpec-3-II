from typing import Any


class Script:
    """Serializable wrapper class for custom interactive scripts."""

    def __init__(self, script_file_name: str) -> None:
        """Initialise a script object.

        Args:
            script_file_name: The filename that the script came from.
        """
        self.file_name = script_file_name

    def get_file_name(self) -> str:
        """Return the filename that the script came from."""
        return self.file_name

    def run(self, params: dict[str, Any]) -> dict[str, Any]:
        """Import and run the script only when needed.

        This keeps Script pickle-serializable for st.cache_data.
        """
        from managers.ScriptManager import ScriptManager

        run_function = ScriptManager.importRunFunction(self.file_name)
        result = run_function(params)

        if not isinstance(result, dict):
            raise TypeError("Script run(params) must return a dictionary.")

        return result
