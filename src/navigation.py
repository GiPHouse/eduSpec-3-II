import json
from pathlib import Path

import streamlit as st

from CustomThemes import THEMES, applyTheme, showThemeSelector
from managers.QuizBuilder import QuizBuilder

# Get the absolute path to the data directory
data_dir = Path(__file__).parent.parent / "data"

# load the top navbar from json
with open(data_dir / "navigation" / "topnavbar.json", 'r') as file:
    TOP_NAV_ITEMS = json.load(file)

def initPage() -> None:
    """Initialize a page"""
    initTheme()
    showNavbar()

def initTheme() -> None:
    """Initialize and apply the current theme."""
    if "theme" not in st.session_state:
        st.session_state["theme"] = "Light"

    applyTheme(THEMES[st.session_state["theme"]])    


def navigate(page: str) -> None:
    """Navigate to a different page

    Args:
        page (str): Name of the page you want to navigate to
    """
    if page is None or page == "None":
        page = "Home"
    st.session_state.current_page = page
    st.query_params["page"] = page  # update url
    st.rerun()

# Top navigation bar
def showNavbar() -> None:
    """Displays the navigation bar that is at the top of the page."""
    labels = [item["label"] for item in TOP_NAV_ITEMS]

    query_params = st.query_params

    if "navbar" not in st.session_state:
        if "page" in query_params:
            page = query_params["page"]
            first_word = page.split(" ")[0]
            if page in labels:
                st.session_state.navbar = page
            elif first_word in labels: # used for the pages with sidebar
                st.session_state.navbar = first_word
            else:
                st.session_state.navbar = "Home"
        else:
            st.session_state.navbar = "Home"

    # show segmented control
    selected = st.segmented_control(
        "",
        labels,
        selection_mode="single",
        key="topnavbar",
        default=st.session_state.navbar
    )

    # update current page if changed
    if selected and selected != st.session_state.navbar:
        st.session_state.current_page = selected
        st.session_state.navbar = selected
        st.query_params["page"] = selected  # update url
        st.rerun() 

# Sidebar Navigation
def sidebarButton(label: str, page: str, indent: int) -> None:
    """Creates a button (with indentation) that is shown in the sidebar.

    The button is used for navigation between pages.
    The type of the button changes when the page is active.

    Args:
        label (str): Text that is shown on the button
        page (str): Name of the page you want to navigate to
        indent (int): Indentation level of the button. Higher value increase the left spacing.

    Returns:
        None
    """
    type_button = "primary" if st.session_state.current_page == page else "tertiary"

    if indent > 0:
        cols = st.sidebar.columns([indent, 20])
        with cols[1]:
            if st.button(label, type=type_button, key=page):
                navigate(page)
    else:
        if st.sidebar.button(label, type=type_button, key=page):
            navigate(page)


def createItemSideBar(items: list, indent: int = 0) -> None:
    """Creates an item in the sidebar

    Args:
        items (list): items that are in the sidebar
        indent (int, optional): Indentation of the item in the sidebar. Defaults to 0.
    """
    for item in items:
        page = item["page"]
        label = item["label"]
        children = item.get("children", [])

        is_active = st.session_state.current_page == page

        child_active = any(
            st.session_state.current_page == child["page"]
            or any(
                st.session_state.current_page == grandchild["page"]
                for grandchild in child.get("children", [])
            )
            for child in children
        )

        sidebarButton(label, page, indent)

        if children and (is_active or child_active):
            createItemSideBar(children, indent + 1)


def createSidebar(nav_structure: dict) -> None:
    """Creates a sidebar based on the input.

    Args:
        nav_structure (dict): Structure + title of the sidebar navigation.
    """
    for section in nav_structure:
        st.sidebar.title(section["title"])
        items = section.get("items", [])
        createItemSideBar(items)