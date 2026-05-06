import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

import streamlit as st

from CustomThemes import THEMES, applyTheme, showThemeSelector

data_dir = Path(__file__).parent.parent / "data" #get path to data directory
navigation_file = data_dir / "navigation" / "navigation.json"
navigation_env_var = "EDUSPEC_NAVIGATION_FILE"

NavigationItem = dict[str, Any]


def getNavigationFile() -> Path:
    """Return the active navigation file path."""
    override = os.getenv(navigation_env_var)
    if override:
        return Path(override)
    return navigation_file


@lru_cache(maxsize=None)
def _loadNavigationItems(navigation_path: str) -> list[NavigationItem]:
    """Load and cache the full navigation tree for a specific file."""
    with open(navigation_path, "r", encoding="utf-8") as file:
        navigation_data = json.load(file)
    return navigation_data["items"]


def loadNavigationItems() -> list[NavigationItem]:
    """Load the full navigation tree."""
    return _loadNavigationItems(str(getNavigationFile().resolve()))


def _walkNavigation(items: list[NavigationItem]) -> list[NavigationItem]:
    """Flatten the navigation tree."""
    nodes: list[NavigationItem] = []
    for item in items:
        nodes.append(item)
        nodes.extend(_walkNavigation(item.get("children", [])))
    return nodes


def getQuestionRegistry() -> list[str]:
    """Return the list of question ids referenced by the navigation tree."""
    #Not sure if we need this function
    valid_question_ids = []
    for item in _walkNavigation(loadNavigationItems()):
        question = item.get("question")
        if question not in valid_question_ids and question is not None:
            valid_question_ids.append(question)
    return valid_question_ids


def getDefaultQuestion() -> str:
    """Return the first question referenced in the navigation tree."""
    nav = _walkNavigation(loadNavigationItems())
    if len(nav) > 0:
        for item in nav:
            question = item.get("question")
            if question is not None:
                return question
    return ""


def itemContainsQuestion(item: NavigationItem, question: str) -> bool:
    """Check whether the item or one of its descendants matches the question."""
    if item.get("question") == question:
        return True

    return any(
        itemContainsQuestion(child, question) for child in item.get("children", [])
    )


def getTopLevelLabel(question: str) -> str:
    """Return the active top-level label for the current question."""
    items = loadNavigationItems()

    for item in items:
        if itemContainsQuestion(item, question):
            return item["label"]

    return items[0]["label"]


def initTheme() -> None:
    """Initialize and apply the current theme."""
    if "theme" not in st.session_state:
        st.session_state["theme"] = "Light"

    applyTheme(THEMES[st.session_state["theme"]])


def navigate(question: str, label: str | None = None) -> None:
    """Navigate to a different question."""
    st.session_state["current_question"] = question
    st.session_state["current_page"] = None
    if label is not None:
        st.session_state["navbar"] = label
    st.query_params["question"] = question
    st.query_params.pop("page", None)
    st.rerun()

def navigateHome() -> None:
    """Navigate to the home page."""
    st.session_state["current_question"] = None
    st.session_state["navbar"] = None
    st.query_params.pop("question", None)
    st.session_state["current_page"] = "home"
    st.query_params["page"] = "home"

def navigatePage(page: str) -> None:
    """Navigate to a different page."""
    st.session_state["current_question"] = None
    st.session_state["navbar"] = None
    st.query_params.pop("question", None)
    st.session_state["current_page"] = page
    st.query_params["page"] = page

def homePage() -> None:
    """render home page"""
    st.title("Live Laugh Learn")
    st.image(str(data_dir / "images" / "maxresdefault.jpg"))
    st.text("In dit huis: maken we geen ruzie, is het altijd gezellig, staat de koffie en thee klaar, staan we voor elkaar klaar")

def settingsPage() -> None:
    """render settings page"""
    st.title("Settings")
    showThemeSelector()

def aboutPage() -> None:
    """render about page"""
    st.title("About")
    st.text("This application was developed by the EduSpec team for educational purposes.")

def renderNavigationButton(
    container: Any, label: str, question: str, current_question: str
) -> None:
    """Render a single navigation button."""
    button_type = "primary" if current_question == question else "secondary"
    if container.button(
        label, key=question, type=button_type, width="stretch"
    ):
        navigate(question, label)


def renderNavigationNode(
    container: Any, item: NavigationItem, current_question: str
) -> None:
    """Render a nested navigation node."""
    children = item.get("children", [])
    question = item.get("question")

    if children:
        expander = container.expander(
            item["label"], expanded=itemContainsQuestion(item, current_question)
        )
        if question:
            renderNavigationButton(expander, item["label"], question, current_question)
        for child in children:
            renderNavigationNode(expander, child, current_question)
        return

    if question:
        renderNavigationButton(container, item["label"], question, current_question)


def showNavigation() -> None:
    """Render the full navigation UI in the sidebar."""
    items = loadNavigationItems()
    current_question = st.session_state.get("current_question", getDefaultQuestion())
    current_label = st.session_state.get("navbar")
    if current_label is not None:
        matching_item = next(
            (item for item in items if item["label"] == current_label),
            None,
        ) 
    else:
        matching_item = None

    if matching_item is not None and itemContainsQuestion(matching_item, current_question):
        st.session_state["navbar"] = current_label
    else:
        st.session_state["navbar"] = getTopLevelLabel(current_question)

    sidebar = st.sidebar
    st.markdown("""
    <style>
    [data-testid="stSidebar"] .stHorizontalBlock {
        display: flex;
        justify-content: start;
        gap: 8px;
    }
    </style>
""", unsafe_allow_html=True)

    with st.sidebar:
        col1, col2, col3 = st.columns(3)
        with col1:
            button_type = "primary" if st.session_state["current_page"] == "home" else "secondary"
            st.button("Home", width="stretch", on_click=navigateHome, type=button_type, key="Home")
        with col2:
            button_type = "primary" if st.session_state["current_page"] == "settings" else "secondary"
            st.button("Settings", width="stretch", on_click=navigatePage, args=("settings",), type=button_type, key="Settings")
        with col3:
            button_type = "primary" if st.session_state["current_page"] == "about" else "secondary"
            st.button("About", width="stretch", on_click=navigatePage, args=("about",), type=button_type, key="About")
        
    tabs = sidebar.tabs([item["label"] for item in items])

    for tab, item in zip(tabs, items):
        with tab:
            question = item.get("question")
            if question:
                renderNavigationButton(tab, item["label"], question, current_question)

            for child in item.get("children", []):
                renderNavigationNode(tab, child, current_question)
