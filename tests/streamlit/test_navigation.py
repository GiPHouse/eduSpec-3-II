from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from streamlit.testing.v1 import AppTest

MOCK_NAVIGATION_FILE = Path(__file__).with_name("mock_navigation.json")


@pytest.fixture(autouse=True)
def use_mock_navigation(monkeypatch: pytest.MonkeyPatch) -> None:
    """Pin navigation tests to a dedicated mock navigation structure."""
    monkeypatch.setenv("EDUSPEC_NAVIGATION_FILE", str(MOCK_NAVIGATION_FILE))


@pytest.fixture(autouse=True)
def mock_question_rendering(monkeypatch: pytest.MonkeyPatch) -> None:
    """Avoid depending on old mock question JSON files in navigation tests."""
    from managers.QuestionManager import QuestionManager
    from QuestionDrawer import QuestionDrawer

    def fake_load_question(question_name: str) -> Any:
        number = question_name.removeprefix("question")
        return SimpleNamespace(
            name=question_name,
            title=f"title{number}",
            bodytext=f"body{number}",
            figures=None,
            body_format="text",
        )

    def fake_draw_question(question: Any) -> None:
        import streamlit as st

        st.title(question.title)

    monkeypatch.setattr(
        QuestionManager,
        "loadQuestion",
        staticmethod(fake_load_question),
    )
    monkeypatch.setattr(
        QuestionDrawer,
        "drawQuestion",
        staticmethod(fake_draw_question),
    )


def run_app() -> AppTest:
    """Create and run the app under test."""
    at = AppTest.from_file("../../src/main.py")
    at.run(timeout=10)
    assert len(at.exception) == 0
    return at


def get_state(at: AppTest, key: str, default: Any = None) -> Any:
    """Read session state safely."""
    try:
        return at.session_state[key]
    except KeyError:
        return default


def click_button(at: AppTest, key: str) -> AppTest:
    """Click a navigation button by its key."""
    at.button(key).click().run(timeout=10)
    assert len(at.exception) == 0
    return at


def assert_query_question(at: AppTest, question: str) -> None:
    """Assert the current query-string question value."""
    assert at.query_params["question"] == [question]


def assert_title(at: AppTest, expected: str) -> None:
    """Assert the rendered main title."""
    assert expected in [title.value for title in at.title]


def test_home_page_default() -> None:
    """Test that the home page is shown when no question is selected."""
    at = run_app()

    assert at.session_state["current_page"] == "home"
    assert get_state(at, "current_question") is None


def test_navigation_to_nmr_question() -> None:
    """Test navigation to the NMR question."""
    at = click_button(run_app(), "question5")

    assert at.session_state["current_question"] == "question5"
    assert at.session_state["navbar"] == "NMR"
    assert_query_question(at, "question5")


def test_navigation_to_ms_question() -> None:
    """Test navigation to the MS question."""
    at = click_button(run_app(), "question6")

    assert at.session_state["current_question"] == "question6"
    assert at.session_state["navbar"] == "MS"
    assert_query_question(at, "question6")


def test_navigation_to_molecule_question() -> None:
    """Test navigation to the molecule question."""
    at = click_button(run_app(), "question7")

    assert at.session_state["current_question"] == "question7"
    assert at.session_state["navbar"] == "Molecules"
    assert_query_question(at, "question7")


def test_navigation_to_word_question() -> None:
    """Test navigation to the word question."""
    at = click_button(run_app(), "question8")

    assert at.session_state["current_question"] == "question8"
    assert at.session_state["navbar"] == "Word"
    assert_query_question(at, "question8")


def test_navigation_to_nested_directory_question() -> None:
    """Test navigation through a nested directory example."""
    at = click_button(run_app(), "question3")

    assert at.session_state["current_question"] == "question3"
    assert at.session_state["navbar"] == "IR"
    assert_query_question(at, "question3")
    assert_title(at, "title3")


def test_url_direct_load_valid_question() -> None:
    """Test loading a valid question via URL query parameter."""
    at = AppTest.from_file("../../src/main.py")
    at.query_params["question"] = "question3"
    at.run(timeout=10)

    assert at.session_state["current_question"] == "question3"
    assert at.session_state["navbar"] == "IR"
    assert_title(at, "title3")


def test_multiple_question_navigations() -> None:
    """Test navigating through multiple question links."""
    at = run_app()

    click_button(at, "question5")
    assert at.session_state["current_question"] == "question5"
    assert at.session_state["navbar"] == "NMR"
    assert_title(at, "title5")

    click_button(at, "question6")
    assert at.session_state["current_question"] == "question6"
    assert at.session_state["navbar"] == "MS"
    assert_title(at, "title6")

    click_button(at, "question7")
    assert at.session_state["current_question"] == "question7"
    assert at.session_state["navbar"] == "Molecules"
    assert_title(at, "title7")


def test_navigation_to_home() -> None:
    """Test navigation back to the home page."""
    at = run_app()

    at.sidebar.button("Home").click().run(timeout=10)

    assert len(at.exception) == 0
    assert get_state(at, "current_question") is None
    assert at.session_state["current_page"] == "home"
    assert at.query_params.get("question") is None
    assert at.query_params.get("page") == ["home"] or at.query_params.get("page") is None


def test_navigation_to_settings() -> None:
    """Test navigation to the settings page."""
    at = click_button(run_app(), "Settings")

    assert get_state(at, "current_question") is None
    assert at.session_state["current_page"] == "settings"
    assert at.query_params.get("question") is None
    assert at.query_params.get("page") == ["settings"]


def test_navigation_to_about() -> None:
    """Test navigation to the about page."""
    at = click_button(run_app(), "About")

    assert get_state(at, "current_question") is None
    assert at.session_state["current_page"] == "about"
    assert at.query_params.get("question") is None
    assert at.query_params.get("page") == ["about"]
