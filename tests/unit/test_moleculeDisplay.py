from pathlib import Path
from unittest.mock import Mock, patch

from MoleculeDisplay import MoleculeDisplay

# Mock is a unit testing tool that lets you temporarily replace things during a test
# because we dont want to open renderers and depend on Streamlit UI each time.


def clear_molecule_display_caches() -> None:
    """Clear Streamlit cache wrappers on MoleculeDisplay methods."""
    MoleculeDisplay.displayProteinById.clear()
    MoleculeDisplay.displayPdbString.clear()
    MoleculeDisplay.displayMoleculeFromFile.clear()
    MoleculeDisplay.drawYourself.clear()


def test_display_protein_by_id_uses_render_pdb_and_showmol() -> None:
    """displayProteinById should render the protein, style it, and show it."""
    clear_molecule_display_caches()

    fake_viewer = Mock()

    with (
        patch("MoleculeDisplay.render_pdb", return_value=fake_viewer) as mock_render_pdb,
        patch("MoleculeDisplay.showmol") as mock_showmol,
    ):
        MoleculeDisplay.displayProteinById(pdb_id="1ABC", style="stick", height=300, width=600)

    mock_render_pdb.assert_called_once_with(id="1ABC")
    fake_viewer.setStyle.assert_called_once_with({}, {"stick": {"colorscheme": "Jmol"}})
    mock_showmol.assert_called_once_with(fake_viewer, height=300, width=600)


def test_display_protein_by_id_unknown_style_falls_back_to_cartoon() -> None:
    """displayProteinById should fall back for an unknown style."""
    clear_molecule_display_caches()

    fake_viewer = Mock()

    with (
        patch("MoleculeDisplay.render_pdb", return_value=fake_viewer),
        patch("MoleculeDisplay.showmol"),
    ):
        MoleculeDisplay.displayProteinById(pdb_id="1ABC", style="unknown")

    fake_viewer.setStyle.assert_called_once_with({}, {"cartoon": {"color": "spectrum"}})


def test_display_pdb_string_builds_viewer_and_renders() -> None:
    """displayPdbString should create a viewer, add the model, style it, zoom, and show it."""
    clear_molecule_display_caches()

    fake_view = Mock()
    pdb_string = "ATOM      1  N   ALA A   1      11.104  13.207   9.310"

    with (
        patch("MoleculeDisplay.py3Dmol.view", return_value=fake_view) as mock_view_factory,
        patch("MoleculeDisplay.showmol") as mock_showmol,
    ):
        MoleculeDisplay.displayPdbString(
            pdb_string=pdb_string,
            style="ballAndStick",
            height=400,
            width=700,
        )

    mock_view_factory.assert_called_once_with(width=700, height=400)
    fake_view.addModel.assert_called_once_with(pdb_string, "pdb")
    fake_view.setStyle.assert_called_once_with(
        {},
        {
            "stick": {"scale": 0.25, "colorscheme": "Jmol"},
            "sphere": {"scale": 0.3},
        },
    )
    fake_view.zoomTo.assert_called_once_with()
    mock_showmol.assert_called_once_with(fake_view, height=400, width=700)


def test_display_pdb_string_unknown_style_falls_back_to_stick() -> None:
    """displayPdbString should fall back to stick style for an unknown style."""
    clear_molecule_display_caches()

    fake_view = Mock()

    with (
        patch("MoleculeDisplay.py3Dmol.view", return_value=fake_view),
        patch("MoleculeDisplay.showmol"),
    ):
        MoleculeDisplay.displayPdbString(pdb_string="TEST", style="unknown")

    fake_view.setStyle.assert_called_once_with({}, {"stick": {"colorscheme": "Jmol"}})


def test_display_molecule_from_file_uses_pdb_for_pdb_extension(tmp_path: Path) -> None:
    """displayMoleculeFromFile should use pdb format for .pdb files."""
    clear_molecule_display_caches()

    pdb_file = tmp_path / "example.pdb"
    pdb_file.write_text("PDB CONTENT", encoding="utf-8")

    fake_view = Mock()

    with (
        patch("MoleculeDisplay.py3Dmol.view", return_value=fake_view) as mock_view_factory,
        patch("MoleculeDisplay.showmol") as mock_showmol,
    ):
        MoleculeDisplay.displayMoleculeFromFile(
            pdb_file_path=str(pdb_file),
            style="sphere",
            height=350,
            width=650,
        )

    mock_view_factory.assert_called_once_with(width=650, height=350)
    fake_view.addModel.assert_called_once_with("PDB CONTENT", "pdb")
    fake_view.setStyle.assert_called_once_with({}, {"sphere": {}})
    fake_view.zoomTo.assert_called_once_with()
    mock_showmol.assert_called_once_with(fake_view, height=350, width=650)


def test_display_molecule_from_file_uses_pdb_for_ent_extension(tmp_path: Path) -> None:
    """displayMoleculeFromFile should use pdb format for .ent files."""
    clear_molecule_display_caches()

    ent_file = tmp_path / "example.ent"
    ent_file.write_text("ENT CONTENT", encoding="utf-8")

    fake_view = Mock()

    with (
        patch("MoleculeDisplay.py3Dmol.view", return_value=fake_view),
        patch("MoleculeDisplay.showmol"),
    ):
        MoleculeDisplay.displayMoleculeFromFile(pdb_file_path=str(ent_file))

    fake_view.addModel.assert_called_once_with("ENT CONTENT", "pdb")


def test_display_molecule_from_file_uses_mol2_for_other_extensions(tmp_path: Path) -> None:
    """displayMoleculeFromFile should use mol2 format for non-pdb-like extensions."""
    clear_molecule_display_caches()

    mol2_file = tmp_path / "example.mol2"
    mol2_file.write_text("MOL2 CONTENT", encoding="utf-8")

    fake_view = Mock()

    with (
        patch("MoleculeDisplay.py3Dmol.view", return_value=fake_view),
        patch("MoleculeDisplay.showmol"),
    ):
        MoleculeDisplay.displayMoleculeFromFile(pdb_file_path=str(mol2_file))

    fake_view.addModel.assert_called_once_with("MOL2 CONTENT", "mol2")


def test_display_molecule_from_file_unknown_style_uses_current_fallback(
    tmp_path: Path,
) -> None:
    """displayMoleculeFromFile should use its current fallback style for unknown styles."""
    clear_molecule_display_caches()

    pdb_file = tmp_path / "example.pdb"
    pdb_file.write_text("PDB CONTENT", encoding="utf-8")

    fake_view = Mock()

    with (
        patch("MoleculeDisplay.py3Dmol.view", return_value=fake_view),
        patch("MoleculeDisplay.showmol"),
    ):
        MoleculeDisplay.displayMoleculeFromFile(pdb_file_path=str(pdb_file), style="unknown")

    fake_view.setStyle.assert_called_once_with({}, {"ballAndStick": {"colorscheme": "Jmol"}})


def test_draw_yourself_renders_valid_file(tmp_path: Path) -> None:
    """drawYourself should render a valid pdb file and not show an error."""
    clear_molecule_display_caches()

    pdb_file = tmp_path / "valid.pdb"
    pdb_file.write_text("VALID PDB", encoding="utf-8")

    fake_view = Mock()

    with (
        patch("MoleculeDisplay.py3Dmol.view", return_value=fake_view) as mock_view_factory,
        patch("MoleculeDisplay.showmol") as mock_showmol,
        patch("MoleculeDisplay.st.error") as mock_error,
    ):
        MoleculeDisplay.drawYourself(imgpath=str(pdb_file))

    mock_view_factory.assert_called_once_with(width=800, height=500)
    fake_view.addModel.assert_called_once_with("VALID PDB", "pdb")
    fake_view.setStyle.assert_called_once_with(
        {},
        {
            "stick": {"scale": 0.25, "colorscheme": "Jmol"},
            "sphere": {"scale": 0.3},
        },
    )
    fake_view.zoomTo.assert_called_once_with()
    mock_showmol.assert_called_once_with(fake_view, height=500, width=800)
    mock_error.assert_not_called()


def test_draw_yourself_shows_error_for_empty_file(tmp_path: Path) -> None:
    """drawYourself should show an error when the pdb file is empty."""
    clear_molecule_display_caches()

    empty_file = tmp_path / "empty.pdb"
    empty_file.write_text("", encoding="utf-8")

    with patch("MoleculeDisplay.st.error") as mock_error:
        MoleculeDisplay.drawYourself(imgpath=str(empty_file))

    mock_error.assert_called_once_with(f"PDB file is empty: {empty_file}")


def test_draw_yourself_shows_error_for_missing_file(tmp_path: Path) -> None:
    """drawYourself should show an error when the pdb file does not exist."""
    clear_molecule_display_caches()

    missing_file = tmp_path / "missing.pdb"

    with patch("MoleculeDisplay.st.error") as mock_error:
        MoleculeDisplay.drawYourself(imgpath=str(missing_file))

    mock_error.assert_called_once_with(f"PDB file not found: {missing_file}")


def test_draw_yourself_shows_error_when_rendering_fails(tmp_path: Path) -> None:
    """drawYourself should show an error when rendering raises an exception."""
    clear_molecule_display_caches()

    pdb_file = tmp_path / "broken.pdb"
    pdb_file.write_text("VALID PDB", encoding="utf-8")

    with (
        patch(
            "MoleculeDisplay.py3Dmol.view",
            side_effect=RuntimeError("boom"),
        ),
        patch("MoleculeDisplay.st.error") as mock_error,
    ):
        MoleculeDisplay.drawYourself(imgpath=str(pdb_file))

    mock_error.assert_called_once_with("Failed to render molecule: boom")
