import py3Dmol
from stmol import render_pdb, showmol


class MoleculeDisplay:
    """Handles 3D interactive molecule display using stmol."""

    @staticmethod
    def displayProteinById(
        pdb_id: str, style: str = "cartoon", height: int = 500, width: int = 800
    ) -> None:
        """Display a protein structure by PDB ID.

        Args:
            pdb_id (str): PDB ID (e.g., '1A2C').
            style (str, optional): Display style - 'cartoon', 'stick', 'sphere'. Defaults to 'cartoon'.
            height (int, optional): Height of the viewer in pixels. Defaults to 500.
            width (int, optional): Width of the viewer in pixels. Defaults to 800.
        """
        viewer = render_pdb(id=pdb_id)

        style_dict = {
            "cartoon": {"cartoon": {"color": "spectrum"}},
            "stick": {"stick": {"colorscheme": "Jmol"}},
            "sphere": {"sphere": {}},
        }

        viewer.setStyle({}, style_dict.get(style, {"cartoon": {"color": "spectrum"}}))
        showmol(viewer, height=height, width=width)

    @staticmethod
    def displayPdbString(
        pdb_string: str, style: str = "stick", height: int = 500, width: int = 800
    ) -> None:
        """Display a molecule defined in PDB

        Args:
            pdb_string (str): The molecule in PDB.
            style (str, optional): Display style. Defaults to "stick".
            height (int, optional): Height of the viewer in pixels. Defaults to 500.
            width (int, optional): Width of the viewer in pixels. Defaults to 800.
        """
        view = py3Dmol.view(width=width, height=height)
        view.addModel(pdb_string, "pdb")
        view.setStyle({style: {}})
        view.zoomTo()
        showmol(view, height=height, width=width)

    @staticmethod
    def displayMoleculeFromFile(
        pdb_file_path: str, style: str = "cartoon", height: int = 500, width: int = 800
    ) -> None:
        """Display a molecule from a PDB file.

        Args:
            pdb_file_path (str): Path to the PDB file.
            style (str, optional): Display style - 'cartoon', 'stick', 'sphere'. Defaults to 'cartoon'.
            height (int, optional): Height of the viewer in pixels. Defaults to 500.
            width (int, optional): Width of the viewer in pixels. Defaults to 800.
        """
        with open(pdb_file_path, "r") as f:
            pdb_string = f.read()

        MoleculeDisplay.displayPdbString(pdb_string, style, height, width)
