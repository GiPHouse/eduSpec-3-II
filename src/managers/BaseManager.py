import pathlib
from os import environ

type DirectoryStructure = list[str | tuple[str, "DirectoryStructure"]]
"""Type for the structure of data directories.

Filenames are stored as strings, directories as a tuple having the directory name first and contents second.
This is recursive, we essentially start in the second item (contents) of the base directory.
"""


class BaseManager:
    """Abstract base manager to handle shared methods and serve as template"""

    # DO NOT MODIFY _data_dir OUTSIDE TESTS
    _data_dir = pathlib.Path("data/")
    data_dir_env_var = "EDUSPEC_DATA_DIR"

    _item_dir: pathlib.Path

    def __init_subclass__(cls) -> None:
        """Make sure item dir is set."""
        super().__init_subclass__()

        if not hasattr(cls, "_item_dir") or not cls._item_dir:
            raise TypeError(f"{cls.__name__} must define '_item_dir'!")

    @classmethod
    def itemExists(cls, item_name: str) -> bool:
        """Checks whether an item exists

        Args:
            item_name (str): The item to check

        Returns:
            bool: Whether it exists on disk
        """
        item_dir = cls._getDir()

        # Most general items are json files
        item_file = item_dir.joinpath(f"{item_name}.json")

        return item_file.is_file()

    @classmethod
    def _getDir(cls) -> pathlib.Path:
        """Returns the directory path

        Returns:
            pathlib.Path: The quiz directory path
        """
        item_dir = cls.getDataDir().joinpath(cls._item_dir)

        if not item_dir.exists():
            item_dir.mkdir(parents=True)
        return item_dir

    @classmethod
    def getDataDir(cls) -> pathlib.Path:
        """Return the configured root data directory."""
        configured_data_dir = (
            environ.get(cls.data_dir_env_var)
            or environ.get("DATA_DIR")
            or environ.get("PATH_FROM_ROOT")
        )
        if configured_data_dir:
            return pathlib.Path(configured_data_dir)

        # We are in <base>/src/managers/BaseManager.py
        current_file = pathlib.Path(__file__)
        # We wish to go up 2 directories (and start from the file)
        base_dir = current_file.parents[2]
        # Now we go down to the general data directory
        return base_dir.joinpath(cls._data_dir)

    @classmethod
    def resolveDataPath(
        cls,
        path: str,
        relative_to: pathlib.Path | None = None,
    ) -> str:
        """Resolve a datasource-relative path to an existing file when possible."""
        resolved_path = pathlib.Path(path)
        if resolved_path.is_absolute() and resolved_path.exists():
            return str(resolved_path)

        data_root = cls.getDataDir()
        path_without_data_prefix = (
            pathlib.Path(*resolved_path.parts[1:])
            if resolved_path.parts and resolved_path.parts[0].lower() == "data"
            else resolved_path
        )

        candidates = []
        if relative_to is not None:
            candidates.append(relative_to / resolved_path)

        candidates.extend(
            [
                data_root / resolved_path,
                data_root / path_without_data_prefix,
                data_root / "images" / resolved_path.name,
                data_root / "molecules" / resolved_path.name,
                data_root / "spectra" / resolved_path.name,
                data_root / "spectra" / resolved_path,
            ]
        )

        for candidate in candidates:
            if candidate.exists():
                return str(candidate.resolve())

        matches = list(data_root.rglob(resolved_path.name)) if data_root.exists() else []
        if len(matches) == 1:
            return str(matches[0].resolve())

        return str(resolved_path)

    @classmethod
    def _iterDir(cls, start: pathlib.Path, enter_subdirs: bool = True) -> DirectoryStructure:
        """Iterates all the items in a directory

        Args:
            start (pathlib.Path): The path to start from.
            enter_subdirs (bool, optional): Whether to enter subdirectories or ignore them. This will return `list[str]` when False. Defaults to False.

        Returns:
            DirectoryStructure: The items, without file extension.
                Directories are tuples with the dir name first and the list of items second.
        """
        out = []
        for item in start.iterdir():
            if item.is_dir():
                out.append((item.name, cls._iterDir(item)))
            else:
                out.append(item.name)
        return out

    @classmethod
    def _iterDirFlat(cls, start: pathlib.Path) -> list[str]:
        """Iterates all the items in a directory, without distinction for subdirectories.

        Args:
            start (pathlib.Path): The path to start from.

        Returns:
            list[str]: All the items in the path and its subdirectories, without file extensions.
        """
        out = []
        for item in start.iterdir():
            if item.is_dir():
                out.extend(cls._iterDirFlat(item))
            else:
                out.append(item.name)
        return out

    @classmethod
    def createDirectory(cls, name: str, path: str = "") -> bool:
        """Creates a directory within the file

        Args:
            name (str): The name of the new directory
            path (str, optional): The parents of the directory, if any. Defaults to "".

        Returns:
            bool: Whether the dir was succesfully created
        """
        base_dir = cls._getDir()

        par_dir = base_dir.joinpath(path).resolve()

        new_dir = par_dir.joinpath(name)
        new_dir.mkdir(parents=False, exist_ok=False)

        return True
