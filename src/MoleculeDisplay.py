import streamlit as st
from stmol import showmol, render_pdb
import py3Dmol


class MoleculeDisplay:
    """Class to handle 3D interactive molecule display using stmol"""
    
    @staticmethod
    def displayProteinById(pdb_id, style='cartoon', height=500, width=800) -> None :
        """
        Display a protein structure by PDB ID
        
        Args:
            pdb_id (str): PDB ID (e.g., '1A2C')
            style (str): Display style - 'cartoon', 'stick', 'sphere'
            height (int): Height of the viewer in pixels
            width (int): Width of the viewer in pixels
        """
        viewer = render_pdb(id=pdb_id)
        
        style_dict = {
            'cartoon': {'cartoon': {'color': 'spectrum'}},
            'stick': {'stick': {'colorscheme': 'Jmol'}},
            'sphere': {'sphere': {}}
        }
        
        viewer.setStyle({}, style_dict.get(style, {'cartoon': {'color': 'spectrum'}}))
        showmol(viewer, height=height, width=width)
    
    @staticmethod
    def displayPdbString(pdb_string: str, style="stick", height=500, width=800):
        view = py3Dmol.view(width=width, height=height)
        view.addModel(pdb_string, "pdb")
        view.setStyle({style: {}})
        view.zoomTo()
        showmol(view, height=height, width=width)
    
    @staticmethod
    def displayMoleculeFromFile(pdb_file_path, style='cartoon', height=500, width=800):
        """
        Display a molecule from a PDB file
        
        Args:
            pdb_file_path (str): Path to the PDB file
            style (str): Display style - 'cartoon', 'stick', 'sphere'
            height (int): Height of the viewer in pixels
            width (int): Width of the viewer in pixels
        """
        with open(pdb_file_path, 'r') as f:
            pdb_string = f.read()
        
        MoleculeDisplay.displayPdbString(pdb_string, style, height, width)
