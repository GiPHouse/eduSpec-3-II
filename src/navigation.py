import json
from pathlib import Path
from typing import Any

import streamlit as st

from CustomThemes import THEMES, applyTheme, showThemeSelector

CURRENT_DIR = Path(__file__).resolve().parent
NAVIGATION_PATH = CURRENT_DIR.parent / "data" / "navigation.json"


def load_navigation_config() -> dict[str, Any]:
    """Load the JSON-backed navigation structure."""
    with NAVIGATION_PATH.open(encoding="utf-8") as navigation_file:
        return json.load(navigation_file)


def flatten_pages(items: list[dict[str, Any]], tab_label: str) -> dict[str, dict[str, str]]:
    """Create a page lookup for the current tab tree."""
    pages: dict[str, dict[str, str]] = {}

    for item in items:
        page = item.get("page")
        if page:
            pages[page] = {
                "label": item["label"],
                "tab": tab_label,
                "description": item.get("description", ""),
            }

        children = item.get("children", [])
        if children:
            pages.update(flatten_pages(children, tab_label))

    return pages


def build_page_index(navigation_config: dict[str, Any]) -> dict[str, dict[str, str]]:
    """Collect every addressable page from the navigation JSON."""
    page_index: dict[str, dict[str, str]] = {}

    for tab in navigation_config["tabs"]:
        page_index.update(flatten_pages([tab], tab["label"]))

    return page_index


def normalise_query_page(page_value: Any) -> str | None:
    """Normalise Streamlit query param values into a single page string."""
    if isinstance(page_value, list):
        return page_value[0] if page_value else None

    if isinstance(page_value, str):
        return page_value

    return None


NAVIGATION_CONFIG = load_navigation_config()
PAGE_INDEX = build_page_index(NAVIGATION_CONFIG)
DEFAULT_PAGE = NAVIGATION_CONFIG.get("default_page", "Home")


def get_requested_page() -> str:
    """Resolve the requested page from the URL, falling back to the default page."""
    requested_page = normalise_query_page(st.query_params.get("page"))

    if requested_page in PAGE_INDEX:
        return requested_page

    return DEFAULT_PAGE


def initialise_navigation_state() -> None:
    """Synchronise session state with the URL search parameter."""
    requested_page = get_requested_page()

    if "current_page" not in st.session_state:
        st.session_state.current_page = requested_page
        return

    if requested_page != st.session_state.current_page:
        st.session_state.current_page = requested_page


def navigate(page: str) -> None:
    """Navigate to a different page and keep the URL in sync."""
    if page not in PAGE_INDEX:
        return

    st.session_state.current_page = page
    st.query_params["page"] = page
    st.rerun()


def is_branch_active(item: dict[str, Any], current_page: str) -> bool:
    """Check whether the current page exists in the given branch."""
    if item.get("page") == current_page:
        return True

    return any(is_branch_active(child, current_page) for child in item.get("children", []))


def render_nav_button(label: str, page: str, key_prefix: str) -> None:
    """Render a navigation button that updates the current page."""
    button_type = "primary" if st.session_state.current_page == page else "tertiary"

    if st.button(label, type=button_type, key=f"{key_prefix}:{page}"):
        navigate(page)


def render_navigation_branch(item: dict[str, Any], key_prefix: str) -> None:
    """Render a nested expander/button branch from the JSON tree."""
    page = item.get("page")
    children = item.get("children", [])

    if children:
        with st.expander(
            item["label"],
            expanded=is_branch_active(item, st.session_state.current_page),
        ):
            if page:
                button_label = item.get("button_label", f"Open {item['label']}")
                render_nav_button(button_label, page, key_prefix)

            for child in children:
                render_navigation_branch(child, f"{key_prefix}/{item['label']}")

        return

    if page:
        button_label = item.get("button_label", item["label"])
        render_nav_button(button_label, page, key_prefix)


def show_sidebar_navigation() -> None:
    """Render all navigation in the sidebar using tabs and nested expanders."""
    current_page = st.session_state.current_page
    current_tab = PAGE_INDEX[current_page]["tab"]
    tab_labels = [tab["label"] for tab in NAVIGATION_CONFIG["tabs"]]
    tab_containers = st.sidebar.tabs(tab_labels, default=current_tab)

    for tab_config, tab_container in zip(NAVIGATION_CONFIG["tabs"], tab_containers):
        with tab_container:
            if tab_config.get("description"):
                st.caption(tab_config["description"])

            if tab_config.get("page"):
                button_label = tab_config.get("button_label", f"Open {tab_config['label']}")
                render_nav_button(button_label, tab_config["page"], f"tab:{tab_config['label']}")

            for child in tab_config.get("children", []):
                render_navigation_branch(child, f"tab:{tab_config['label']}")


def render_placeholder_page(page: str) -> None:
    """Render the currently selected page."""
    page_config = PAGE_INDEX[page]
    st.title(page_config["label"])

    if page_config["description"]:
        st.caption(page_config["description"])

    if page == "Setting":
        st.subheader("Theme")
        showThemeSelector()


if "theme" not in st.session_state:
    st.session_state["theme"] = "Light"

applyTheme(THEMES[st.session_state["theme"]])
initialise_navigation_state()
show_sidebar_navigation()
render_placeholder_page(st.session_state.current_page)
