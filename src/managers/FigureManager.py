from pathlib import Path

from streamlit import cache_data

from managers.BaseManager import BaseManager


class FigureManager(BaseManager):
    """Class for loading figures from/to the file system"""

    supported_item_dirs = {
        ".png": Path("images"),
        ".jpg": Path("images"),
        ".jpeg": Path("images"),
        ".mol": Path("molecules"),
        ".pdb": Path("molecules"),
        ".jdx": Path("spectra"),
        ".dx": Path("spectra"),
    }
    _item_dir = "default"

    @classmethod
    def _detect_type_and_set_item_dir(cls, name: str) -> str:
        """Detects the type of the provided file and adjusts the scope of the Figure Manager accordingly.

        Args:
            name (str): filename (with extension)

        Raises:
            ValueError: Raises if the file has an unsupported extension.
        """
        ext = Path(name).suffix.lower()
        if ext not in cls.supported_item_dirs:
            raise ValueError(
                f"The extension: {ext} for the provided file: {name} is not supported yet. Please refer to FigureManager implementation"
            )

        cls._item_dir = cls.supported_item_dirs[ext]

        return ext

    @classmethod
    @cache_data
    def loadFigure(cls, name: str) -> bytes:
        """Loads a figure from its name.

        Args:
            name (str): The unique filename of the figure to load.

        Raises:
            FileNotFound: When trying to load a figure that doesn't exist.
            TypeError: When building an unrecognised figure type and its path isn't provided.

        Returns:
            bytes: The pure bytes of the figure, to be decoded by the classes that want to use it.
        """
        cls._detect_type_and_set_item_dir(name)
        if not cls.itemExists(name, file_extension=""):
            raise FileNotFoundError(f"Figure {name} does not exist!, full itemdir: {cls._item_dir}")
        data_dir = cls._getDir()
        figure_file_path = data_dir.joinpath(f"{name}")

        figure_data = figure_file_path.read_bytes()

        return figure_data

    @classmethod
    def saveFigure(cls, figure: bytes, name: str) -> bool:
        """Saves a figure to the file system. Use `updateFigure()` to change an existing one.

        Raises:
            FileExistsError: When trying to save a duplicate figure.

        Args:
            figure (bytes): The figure to save.
            name (str): The name of the figure

        Returns:
            bool: Whether saving was succesful.
        """
        cls._detect_type_and_set_item_dir(name)

        if cls.itemExists(name, file_extension=""):
            raise FileExistsError(f"Figure {name} already exists!")

        data_dir = cls._getDir()
        figure_file_path = data_dir.joinpath(f"{name}")
        figure_file_path.write_bytes(figure)
        return True

    @classmethod
    def updateFigure(cls, figure: bytes, name: str) -> bool:
        """Updates a figure in the file system. Use `saveFigure()` to save a new one.

        Args:
            figure (bytes): The new figure data
            name (str): The name of the figure to update

        Raises:
            FileExistsError: When trying to update something that does not exist

        Returns:
            bool: Whether the update was succesful.
        """
        cls._detect_type_and_set_item_dir(name)
        if not cls.itemExists(name, file_extension=""):
            raise FileExistsError(
                f"Figure {name} does not exist! Maybe you wanted to use FigureManager.saveFigure()?"
            )
        data_dir = cls._getDir()
        figure_file_path = data_dir.joinpath(f"{name}")
        figure_file_path.write_bytes(figure)
        return True
