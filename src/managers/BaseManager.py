import pathlib
from os import environ


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
