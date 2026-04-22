import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

import streamlit as st

from CustomThemes import THEMES, applyTheme

data_dir = Path(__file__).parent.parent / "data"
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


def getQuestionRegistry() -> set[str]:
    """Return the set of question ids referenced by the navigation tree."""
    return {
        item["question"]
        for item in _walkNavigation(loadNavigationItems())
        if item.get("question")
    }


def getDefaultQuestion() -> str:
    """Return the first question referenced in the navigation tree."""
    for item in _walkNavigation(loadNavigationItems()):
        question = item.get("question")
        if question:
            return question
    return ""


def _normaliseQuestionValue(question: str | Iterable[str] | None) -> str | None:
    """Normalise a query/session value to a single question id string."""
    if question is None:
        return None

    if isinstance(question, str):
        return question

    for value in question:
        if value:
            return value

    return None


def resolveQuestion(question: str | Iterable[str] | None) -> str:
    """Resolve a question id to a valid question."""
    normalised_question = _normaliseQuestionValue(question)

    if normalised_question is None or normalised_question == "None":
        return getDefaultQuestion()

    if normalised_question in getQuestionRegistry():
        return normalised_question
    return getDefaultQuestion()


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
    resolved_question = resolveQuestion(question)
    st.session_state["current_question"] = resolved_question
    if label is not None:
        st.session_state["navbar"] = label
    st.query_params["question"] = resolved_question
    st.rerun()


def renderNavigationButton(
    container: Any, label: str, question: str, current_question: str
) -> None:
    """Render a single navigation button."""
    button_type = "primary" if current_question == question else "secondary"
    if container.button(
        label, key=f"nav::{label}", type=button_type, width="stretch"
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
    sidebar.title("Navigation")
    tabs = sidebar.tabs([item["label"] for item in items])

    for tab, item in zip(tabs, items):
        with tab:
            question = item.get("question")
            if question:
                renderNavigationButton(tab, item["label"], question, current_question)

            for child in item.get("children", []):
                renderNavigationNode(tab, child, current_question)
