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
        # When running inside a container we can access a volume from root instead of relative from the file
        if environ.get("PATH_FROM_ROOT", False):
            # We can immediately start from root and go to the general data directory as given in the ENV
            data_dir = pathlib.Path(environ.get("PATH_FROM_ROOT", "/data/"))
            # Then just go to the item-specific dir
            item_dir = data_dir.joinpath(cls._item_dir)
        else:
            # We are in <base>/src/managers/BaseManager.py
            current_file = pathlib.Path(__file__)
            # We wish to go up 2 directories (and start from the file)
            base_dir = current_file.parents[2]
            # Now we go down to the general data directory
            data_dir = base_dir.joinpath(cls._data_dir)
            # And finally to the item-specific one
            item_dir = data_dir.joinpath(cls._item_dir)

        if not item_dir.exists():
            item_dir.mkdir(parents=True)
        return item_dir

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
