"""_summary_

Returns:
_type_: _description_
"""

import os
from typing import Optional

import streamlit.components.v1 as components

_RELEASE = True  # set False when developing locally

if not _RELEASE:
    _component_func = components.declare_component(
        "jsme_component",
        url="http://localhost:3001",
    )
else:
    # when deployed or packaged, serve the built frontend files
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend")
    _component_func = components.declare_component("jsme_component", path=build_dir)


def jsme_component(default_smiles: str = "", key: Optional[str] = None) -> dict | None:
    """Streamlit wrapper function for JSME molecule editor component.

    Args:
        default_smiles: Starting SMILES string to load in the editor.
        key: Optional key for the component

    Returns:
        Dictionary containing 'smiles', 'molfile', and 'jme' strings,
        or None if no molecule has been drawn yet.
    """
    # Call the component frontend and pass any default SMILES
    molecule_data = _component_func(default_smiles=default_smiles, key=key, default=None)

    return molecule_data
