from typing import Any
from unittest.mock import patch

from CustomThemes import THEMES, applyTheme, showThemeSelector


class DummyContext:
    """Simple context manager used to mock Streamlit columns."""

    def __enter__(self) -> "DummyContext":
        """Enter the context."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: Any,
    ) -> bool:
        """Exit the context without suppressing exceptions."""
        return False


def test_apply_theme_calls_html_once() -> None:
    """applyTheme should call st.html once with generated CSS."""
    theme = THEMES["Light"]

    with patch("CustomThemes.st.html") as mock_html:
        applyTheme(theme)

    assert mock_html.call_count == 1
    css = mock_html.call_args.args[0]
    assert ".stApp" in css
    assert theme["backgroundColor"] in css
    assert theme["textColor"] in css
    assert theme["primaryColor"] in css
    assert theme["secondaryBackgroundColor"] in css
    assert theme["borderColor"] in css
    assert theme["buttonColor"] in css
    assert theme["inputBackground"] in css


def test_apply_theme_includes_expected_css_sections() -> None:
    """applyTheme should include key CSS sections for the app."""
    theme = THEMES["Spotify"]

    with patch("CustomThemes.st.html") as mock_html:
        applyTheme(theme)

    css = mock_html.call_args.args[0]
    assert '[data-testid="stSidebar"]' in css
    assert ".stButton > button" in css
    assert ".stSelectbox > div > div" in css
    assert '.stTabs [aria-selected="true"]' in css
    assert '[data-testid="stMetricValue"]' in css
    assert ".stAlert" in css
    assert '[data-testid="stToolbar"]' in css
    assert '[data-testid="stHeader"]' in css


def test_show_theme_selector_sets_default_theme_when_missing() -> None:
    """showThemeSelector should initialise the theme to Light when missing."""
    fake_session_state: dict[str, Any] = {}
    fake_columns = [DummyContext() for _ in range(len(THEMES))]

    with (
        patch("CustomThemes.st.session_state", fake_session_state),
        patch("CustomThemes.applyTheme") as mock_apply_theme,
        patch("CustomThemes.st.markdown"),
        patch("CustomThemes.st.columns", return_value=fake_columns),
        patch("CustomThemes.st.html"),
        patch("CustomThemes.st.button", return_value=False),
        patch("CustomThemes.st.rerun") as mock_rerun,
    ):
        showThemeSelector()

    assert fake_session_state["theme"] == "Light"
    assert mock_apply_theme.call_count == 1
    assert mock_apply_theme.call_args.args == (THEMES["Light"],)
    assert mock_rerun.call_count == 0


def test_show_theme_selector_uses_existing_theme() -> None:
    """showThemeSelector should apply the currently selected theme."""
    fake_session_state: dict[str, Any] = {"theme": "Orange"}
    fake_columns = [DummyContext() for _ in range(len(THEMES))]

    with (
        patch("CustomThemes.st.session_state", fake_session_state),
        patch("CustomThemes.applyTheme") as mock_apply_theme,
        patch("CustomThemes.st.markdown"),
        patch("CustomThemes.st.columns", return_value=fake_columns),
        patch("CustomThemes.st.html"),
        patch("CustomThemes.st.button", return_value=False),
    ):
        showThemeSelector()

    assert fake_session_state["theme"] == "Orange"
    assert mock_apply_theme.call_count == 1
    assert mock_apply_theme.call_args.args == (THEMES["Orange"],)


def test_show_theme_selector_renders_headings() -> None:
    """showThemeSelector should render the title and divider markdown."""
    fake_session_state: dict[str, Any] = {"theme": "Light"}
    fake_columns = [DummyContext() for _ in range(len(THEMES))]

    with (
        patch("CustomThemes.st.session_state", fake_session_state),
        patch("CustomThemes.applyTheme"),
        patch("CustomThemes.st.markdown") as mock_markdown,
        patch("CustomThemes.st.columns", return_value=fake_columns),
        patch("CustomThemes.st.html"),
        patch("CustomThemes.st.button", return_value=False),
    ):
        showThemeSelector()

    assert mock_markdown.call_count == 2
    assert mock_markdown.call_args_list[0].args == ("Choose a Theme",)
    assert mock_markdown.call_args_list[1].args == ("---",)


def test_show_theme_selector_creates_one_column_per_theme() -> None:
    """showThemeSelector should create one column for each theme."""
    fake_session_state: dict[str, Any] = {"theme": "Light"}
    fake_columns = [DummyContext() for _ in range(len(THEMES))]

    with (
        patch("CustomThemes.st.session_state", fake_session_state),
        patch("CustomThemes.applyTheme"),
        patch("CustomThemes.st.markdown"),
        patch("CustomThemes.st.columns", return_value=fake_columns) as mock_columns,
        patch("CustomThemes.st.html"),
        patch("CustomThemes.st.button", return_value=False),
    ):
        showThemeSelector()

    assert mock_columns.call_count == 1
    assert mock_columns.call_args.args == (len(THEMES),)


def test_show_theme_selector_renders_one_preview_per_theme() -> None:
    """showThemeSelector should render one HTML preview swatch per theme."""
    fake_session_state: dict[str, Any] = {"theme": "Light"}
    fake_columns = [DummyContext() for _ in range(len(THEMES))]

    with (
        patch("CustomThemes.st.session_state", fake_session_state),
        patch("CustomThemes.applyTheme"),
        patch("CustomThemes.st.markdown"),
        patch("CustomThemes.st.columns", return_value=fake_columns),
        patch("CustomThemes.st.html") as mock_html,
        patch("CustomThemes.st.button", return_value=False),
    ):
        showThemeSelector()

    assert mock_html.call_count == len(THEMES)


def test_show_theme_selector_marks_active_theme_button() -> None:
    """showThemeSelector should prefix the active theme button label with a tick."""
    fake_session_state: dict[str, Any] = {"theme": "Spotify"}
    fake_columns = [DummyContext() for _ in range(len(THEMES))]

    with (
        patch("CustomThemes.st.session_state", fake_session_state),
        patch("CustomThemes.applyTheme"),
        patch("CustomThemes.st.markdown"),
        patch("CustomThemes.st.columns", return_value=fake_columns),
        patch("CustomThemes.st.html"),
        patch("CustomThemes.st.button", return_value=False) as mock_button,
    ):
        showThemeSelector()

    labels = [call.args[0] for call in mock_button.call_args_list]
    assert "✓ Spotify" in labels
    assert "Light" in labels
    assert "Orange" in labels
    assert "Blue Tint" in labels


def test_show_theme_selector_uses_expected_button_keys_and_width() -> None:
    """showThemeSelector should use the expected button keys and width."""
    fake_session_state: dict[str, Any] = {"theme": "Light"}
    fake_columns = [DummyContext() for _ in range(len(THEMES))]

    with (
        patch("CustomThemes.st.session_state", fake_session_state),
        patch("CustomThemes.applyTheme"),
        patch("CustomThemes.st.markdown"),
        patch("CustomThemes.st.columns", return_value=fake_columns),
        patch("CustomThemes.st.html"),
        patch("CustomThemes.st.button", return_value=False) as mock_button,
    ):
        showThemeSelector()

    expected_keys = {f"theme_btn_{theme_name}" for theme_name in THEMES}
    actual_keys = {call.kwargs["key"] for call in mock_button.call_args_list}
    actual_widths = [call.kwargs["width"] for call in mock_button.call_args_list]

    assert actual_keys == expected_keys
    assert all(width == "stretch" for width in actual_widths)


def test_show_theme_selector_clicking_theme_updates_session_state_and_reruns() -> None:
    """showThemeSelector should update the selected theme and rerun when a button is clicked."""
    fake_session_state: dict[str, Any] = {"theme": "Light"}
    fake_columns = [DummyContext() for _ in range(len(THEMES))]

    def fake_button(label: str, **kwargs: Any) -> bool:
        """Simulate clicking only the Orange theme button."""
        return label == "Orange"

    with (
        patch("CustomThemes.st.session_state", fake_session_state),
        patch("CustomThemes.applyTheme"),
        patch("CustomThemes.st.markdown"),
        patch("CustomThemes.st.columns", return_value=fake_columns),
        patch("CustomThemes.st.html"),
        patch("CustomThemes.st.button", side_effect=fake_button),
        patch("CustomThemes.st.rerun") as mock_rerun,
    ):
        showThemeSelector()

    assert fake_session_state["theme"] == "Orange"
    assert mock_rerun.call_count == 1


def test_show_theme_selector_preview_border_uses_active_highlight() -> None:
    """showThemeSelector should highlight the active theme preview border."""
    fake_session_state: dict[str, Any] = {"theme": "Spotify"}
    fake_columns = [DummyContext() for _ in range(len(THEMES))]

    with (
        patch("CustomThemes.st.session_state", fake_session_state),
        patch("CustomThemes.applyTheme"),
        patch("CustomThemes.st.markdown"),
        patch("CustomThemes.st.columns", return_value=fake_columns),
        patch("CustomThemes.st.html") as mock_html,
        patch("CustomThemes.st.button", return_value=False),
    ):
        showThemeSelector()

    html_blocks = [call.args[0] for call in mock_html.call_args_list]
    spotify_block = next(
        block for block in html_blocks if THEMES["Spotify"]["primaryColor"] in block
    )
    light_block = next(block for block in html_blocks if THEMES["Light"]["primaryColor"] in block)

    assert "border: 2px solid #FF4B4B" in spotify_block
    assert f"border: 2px solid {THEMES['Light']['borderColor']}" in light_block
