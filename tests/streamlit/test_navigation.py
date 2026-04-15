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


def click_label(at: AppTest, label: str) -> AppTest:
    """Click a navigation button by its label."""
    at.button(f"nav::{label}").click().run()
    return at


def assert_query_question(at: AppTest, question: str) -> None:
    """Assert the current query-string question value."""
    assert at.query_params["question"] == [question]


def assert_title(at: AppTest, expected: str) -> None:
    """Assert the rendered main title."""
    assert expected in [title.value for title in at.title]


def test_default_question_selection() -> None:
    """Test the default question and active tab."""
    at = run_app()
    assert at.session_state["current_question"] == "question2"
    assert at.session_state["navbar"] == "IR"
    assert_query_question(at, "question2")
    assert_title(at, "title2")


def test_navigation_to_nmr_question() -> None:
    """Test navigation to the NMR question."""
    at = click_label(run_app(), "NMR")
    assert at.session_state["current_question"] == "question3"
    assert at.session_state["navbar"] == "NMR"
    assert_query_question(at, "question3")
    assert_title(at, "title3")


def test_navigation_to_ms_question() -> None:
    """Test navigation to the MS question."""
    at = click_label(run_app(), "MS")
    assert at.session_state["current_question"] == "question2"
    assert at.session_state["navbar"] == "MS"
    assert_query_question(at, "question2")
    assert_title(at, "title2")


def test_navigation_to_molecule_question() -> None:
    """Test navigation to the molecule question."""
    at = click_label(run_app(), "Molecules")
    assert at.session_state["current_question"] == "question3"
    assert at.session_state["navbar"] == "Molecules"
    assert_query_question(at, "question3")
    assert_title(at, "title3")


def test_navigation_to_word_question() -> None:
    """Test navigation to the word question."""
    at = click_label(run_app(), "Word")
    assert at.session_state["current_question"] == "question2"
    assert at.session_state["navbar"] == "Word"
    assert_query_question(at, "question2")
    assert_title(at, "title2")


def test_navigation_to_nested_directory_question() -> None:
    """Test navigation through a nested directory example."""
    at = click_label(run_app(), "Practice Set")
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

    click_label(at, "NMR")
    assert at.session_state["current_question"] == "question3"
    assert at.session_state["navbar"] == "NMR"
    assert_title(at, "title3")

    click_label(at, "MS")
    assert at.session_state["current_question"] == "question2"
    assert at.session_state["navbar"] == "MS"
    assert_title(at, "title2")

    click_label(at, "Molecules")
    assert at.session_state["current_question"] == "question3"
    assert at.session_state["navbar"] == "Molecules"
    assert_title(at, "title3")
