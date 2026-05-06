from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

MOCK_NAVIGATION_FILE = Path(__file__).with_name("mock_navigation.json")


@pytest.fixture(autouse=True)
def use_mock_navigation(monkeypatch: pytest.MonkeyPatch) -> None:
    """Pin navigation tests to a dedicated mock navigation structure."""
    monkeypatch.setenv("EDUSPEC_NAVIGATION_FILE", str(MOCK_NAVIGATION_FILE))


def run_app() -> AppTest:
    """Create and run the app under test."""
    at = AppTest.from_file("../../src/main.py")
    at.run(timeout=10)
    return at


def click_button(at: AppTest, key: str) -> AppTest:
    """Click a navigation button by its key."""
    at.button(key).click().run()
    return at


def assert_query_question(at: AppTest, question: str) -> None:
    """Assert the current query-string question value."""
    assert at.query_params["question"] == [question]


def assert_title(at: AppTest, expected: str) -> None:
    """Assert the rendered main title."""
    assert expected in [title.value for title in at.title]


# def test_default_question_selection() -> None:
#     """Test the default question and active tab."""
#     at = run_app()
#     assert at.session_state["current_question"] == "question2"
#     assert at.session_state["navbar"] == "IR"
#     assert_query_question(at, "question2")

def test_home_page_default() -> None:
    """Test that the home page is shown when no question is selected."""
    at = AppTest.from_file("../../src/main.py")
    at.run()
    assert at.session_state["current_page"] == "home"
    assert at.session_state["current_question"] is None


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
    at.run()
    assert at.session_state["current_question"] == "question3"
    assert at.session_state["navbar"] == "IR"
    assert_title(at, "title3")


def test_url_direct_load_with_none() -> None:
    """Test that question None defaults to the first configured question."""
    at = AppTest.from_file("../../src/main.py")
    at.query_params["question"] = "None"
    at.run()
    assert at.session_state["current_question"] == "question2"
    assert at.session_state["navbar"] == "IR"
    assert_title(at, "title2")


def test_url_direct_load_invalid_question() -> None:
    """Test that an invalid question defaults to the first configured question."""
    at = AppTest.from_file("../../src/main.py")
    at.query_params["question"] = "does-not-exist"
    at.run()
    assert at.session_state["current_question"] == "question2"
    assert at.session_state["navbar"] == "IR"
    assert_title(at, "title2")


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
    at = AppTest.from_file("../../src/main.py")
    at.run()
    at.sidebar.button("Home").click().run()
    assert at.session_state["current_question"] is None
    assert at.session_state["current_page"] == "home"
    assert at.query_params.get("question") is None
    assert at.query_params.get("page") == ["home"] or at.query_params.get("page") is None


def test_navigation_to_settings() -> None:
    """Test navigation to the settings page."""
    at = click_button(run_app(), "Settings")
    assert at.session_state["current_question"] is None
    assert at.session_state["current_page"] == "settings"
    assert at.query_params.get("question") is None
    assert at.query_params.get("page") == ["settings"]


def test_navigation_to_about() -> None:
    """Test navigation to the about page."""
    at = click_button(run_app(), "About")
    assert at.session_state["current_question"] is None
    assert at.session_state["current_page"] == "about"
    assert at.query_params.get("question") is None
    assert at.query_params.get("page") == ["about"]
