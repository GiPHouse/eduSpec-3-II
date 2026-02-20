"""molecule_drawer.py

Reusable Streamlit molecule drawer using StreamJSME.
Returns a SMILES string.
"""

from dataclasses import dataclass
from typing import Optional

import streamlit as st
from StreamJSME import StreamJSME


@dataclass
class MoleculeDrawerConfig:
    """moleculedrawer"""

    title: str = "JSME Molecule Drawer"
    help_text: Optional[str] = "Draw a molecule. The editor returns a SMILES string."
    default_smiles: str = "N[CH](C)C(=O)O"
    show_output_box: bool = True


class MoleculeDrawer:
    """class"""

    def __init__(self, config: Optional[MoleculeDrawerConfig] = None) -> None:
        """initialisation

        Args:
            config (Optional[MoleculeDrawerConfig], optional): _description_. Defaults to None.
        """
        self.config = config or MoleculeDrawerConfig()

    def render(self, *, key: str = "jsme_main") -> str:
        """Question renderer

        Args:
            key (str, optional): _description_. Defaults to "jsme_main".

        Returns:
            str: _description_
        """
        if self.config.title:
            st.subheader(self.config.title)
        if self.config.help_text:
            st.caption(self.config.help_text)

        # StreamJSME returns the updated SMILES
        try:
            smiles = StreamJSME(smiles=self.config.default_smiles, key=key)
        except TypeError:
            # Some versions don't accept Streamlit's key argument
            smiles = StreamJSME(smiles=self.config.default_smiles)

        if smiles is None:
            smiles = ""

        if self.config.show_output_box:
            st.markdown("### Your SMILES Output:")
            if smiles.strip():
                st.code(smiles, language="text")
            else:
                st.info("Draw something to get a SMILES output.")

        return smiles
