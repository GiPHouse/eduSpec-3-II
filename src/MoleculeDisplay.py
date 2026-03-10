import os

import py3Dmol
import streamlit as st
from stmol import render_pdb, showmol


class MoleculeDisplay:
    """Handles 3D interactive molecule display using stmol."""

    @st.cache_data
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
            "ballAndStick": {
                "stick": {"colorscheme": "Jmol"},
                "sphere": {"scale": 0.3},
            },
        }

        viewer.setStyle({}, style_dict.get(style, {"cartoon": {"color": "spectrum"}}))
        showmol(viewer, height=height, width=width)

    @st.cache_data
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

        style_dict = {
            "cartoon": {"cartoon": {"color": "spectrum"}},
            "stick": {"stick": {"colorscheme": "Jmol"}},
            "sphere": {"sphere": {}},
            "ballAndStick": {
                "stick": {"scale": 0.25, "colorscheme": "Jmol"},
                "sphere": {"scale": 0.3},
            },
        }

        view.setStyle({}, style_dict.get(style, {"stick": {"colorscheme": "Jmol"}}))
        view.zoomTo()
        showmol(view, height=height, width=width)

    @st.cache_data
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
            mol_string = f.read()

        ext = os.path.splitext(pdb_file_path)[1].lower()
        mol_format = "pdb" if ext in [".pdb", ".ent"] else "mol2"

        view = py3Dmol.view(width=width, height=height)
        view.addModel(mol_string, mol_format)

        style_dict = {
            "cartoon": {"cartoon": {"color": "spectrum"}},
            "stick": {"stick": {"colorscheme": "Jmol"}},
            "sphere": {"sphere": {}},
            "ballAndStick": {
                "stick": {"scale": 0.25, "colorscheme": "Jmol"},
                "sphere": {"scale": 0.3},
            },
        }

        view.setStyle({}, style_dict.get(style, {"ballAndStick": {"colorscheme": "Jmol"}}))
        view.zoomTo()
        showmol(view, height=height, width=width)

    @staticmethod
    @st.cache_data
    def drawYourself(imgpath: str) -> None:
        """_summary_

        Args:
            imgpath (str): _description_
        """
        try:
            with open(imgpath, "r") as f:
                mol_string = f.read()

            if not mol_string.strip():
                st.error(f"PDB file is empty: {imgpath}")
                return

            view = py3Dmol.view(width=800, height=500)
            view.addModel(mol_string, "pdb")
            view.setStyle(
                {}, {"stick": {"scale": 0.25, "colorscheme": "Jmol"}, "sphere": {"scale": 0.3}}
            )
            view.zoomTo()
            showmol(view, height=500, width=800)

        except FileNotFoundError:
            st.error(f"PDB file not found: {imgpath}")
        except Exception as e:
            st.error(f"Failed to render molecule: {e}")
