import os
from pathlib import Path
from typing import Optional

import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "jsme_component",
        url="http://localhost:3001",
    )
else:
    frontend_dir = Path(__file__).parent / "pages" / "jsme_component" / "frontend"
    _component_func = components.declare_component(
        "jsme_component", path=os.fspath(frontend_dir)
    )


def jsme_component(default_smiles: str = "", key: Optional[str] = None) -> dict | None:
    """Streamlit wrapper for the JSME molecule editor component."""
    return _component_func(default_smiles=default_smiles, key=key, default=None)
