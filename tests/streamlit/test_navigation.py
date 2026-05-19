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

    def fake_draw_question(
        question: Any,
        quiz: Any | None = None,
        question_index: int | None = None,
    ) -> None:
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


@pytest.fixture(autouse=True)
def mock_quiz_loading(monkeypatch: pytest.MonkeyPatch) -> None:
    """Avoid depending on real quiz JSON files in navigation tests."""
    from managers.QuizManager import QuizManager
    from Quiz import Quiz

    def fake_load_quiz(quiz_name: str) -> Quiz:
        question = SimpleNamespace(
            name=quiz_name,
            title=f"title{quiz_name}",
            bodytext=f"body{quiz_name}",
            figures=None,
            body_format="text",
        )
        return Quiz(quiz_name, [question])

    monkeypatch.setattr(
        QuizManager,
        "loadQuiz",
        staticmethod(fake_load_quiz),
    )


def run_app() -> AppTest:
    """Create and run the app under test."""
    at = AppTest.from_file("../../src/main.py")
    at.run(timeout=10)
    assert len(at.exception) == 0
    return at


def get_state(at: AppTest, key: str) -> Any:
    """Read session state safely."""
    try:
        return at.session_state[key]
    except KeyError:
        return None


def click_button(at: AppTest, key: str) -> AppTest:
    """Click a navigation button by its key."""
    at.button(key).click().run(timeout=10)
    assert len(at.exception) == 0
    return at


def assert_query_question(at: AppTest, question: str) -> None:
    """Assert the current query-string question value."""
    assert at.query_params["question"] == [question]


def assert_query_quiz(at: AppTest, quiz: str) -> None:
    """Assert the current query-string quiz value."""
    assert at.query_params["quiz"] == [quiz]


def assert_title(at: AppTest, expected: str) -> None:
    """Assert the rendered main title."""
    assert expected in [title.value for title in at.title]


def test_home_page_default() -> None:
    """Test that the home page is shown when no question is selected."""
    at = run_app()

    assert get_state(at, "current_page") == "home" 
    assert get_state(at, "current_question") is None
    assert get_state(at, "current_quiz") is None
    assert get_state(at, "navbar") is None 
    assert "quiz" not in at.query_params or at.query_params.get("quiz") is None
    assert "question" not in at.query_params or at.query_params.get("question") is None


def test_navigation_to_nmr_question() -> None:
    """Test navigation to the NMR question."""
    at = click_button(run_app(), "nmr_oxygen_shift_mcq")
    assert get_state(at, "current_question") == "nmr_oxygen_shift_mcq"
    assert get_state(at, "navbar") == "NMR"
    assert get_state(at, "current_quiz") is None 
    assert get_state(at, "current_page") is None
    assert_query_question(at, "nmr_oxygen_shift_mcq")
    assert "quiz" not in at.query_params or at.query_params.get("quiz") is None
    assert "page" not in at.query_params or at.query_params.get("page") is None


def test_navigation_to_ms_question() -> None:
    """Test navigation to the MS question."""
    at = click_button(run_app(), "ms_molecular_ion_mcq")
    assert get_state(at, "navbar") == "MS"
    assert get_state(at, "current_question") == "ms_molecular_ion_mcq"
    assert get_state(at, "current_quiz") is None 
    assert get_state(at, "current_page") is None
    assert_query_question(at, "ms_molecular_ion_mcq")
    assert "quiz" not in at.query_params or at.query_params.get("quiz") is None
    assert "page" not in at.query_params or at.query_params.get("page") is None


def test_navigation_to_molecule_question() -> None:
    """Test navigation to the molecule question."""
    at = click_button(run_app(), "combo_unknown_a_mcq")
    assert get_state(at, "current_question") == "combo_unknown_a_mcq"
    assert get_state(at, "navbar") == "Combination exercises"
    assert get_state(at, "current_quiz") is None 
    assert get_state(at, "current_page") is None
    assert_query_question(at, "combo_unknown_a_mcq")
    assert "quiz" not in at.query_params or at.query_params.get("quiz") is None
    assert "page" not in at.query_params or at.query_params.get("page") is None


def test_navigation_to_word_question() -> None:
    """Test navigation to the word question."""
    at = click_button(run_app(), "nmr_terminal_methyl_word")
    assert get_state(at, "current_question") == "nmr_terminal_methyl_word"
    assert get_state(at, "navbar") == "NMR"
    assert get_state(at, "current_quiz") is None 
    assert get_state(at, "current_page") is None
    assert_query_question(at, "nmr_terminal_methyl_word")
    assert "quiz" not in at.query_params or at.query_params.get("quiz") is None
    assert "page" not in at.query_params or at.query_params.get("page") is None


def test_navigation_to_nested_directory_question() -> None:
    """Test navigation through a nested directory example."""
    at = click_button(run_app(), "ir_c_o_stretch_click")
    assert get_state(at, "current_question") == "ir_c_o_stretch_click"
    assert get_state(at, "navbar") == "IR"
    assert get_state(at, "current_quiz") is None 
    assert get_state(at, "current_page") is None
    assert_query_question(at, "ir_c_o_stretch_click")
    assert_title(at, "titleir_c_o_stretch_click")
    assert "quiz" not in at.query_params or at.query_params.get("quiz") is None
    assert "page" not in at.query_params or at.query_params.get("page") is None

def test_navigation_to_quiz() -> None:
    """Test navigation to a quiz page."""
    at = click_button(run_app(), "quiz_nmr_quiz")

    assert get_state(at, "current_quiz") == "nmr_quiz"
    assert get_state(at, "navbar") == "NMR"
    assert get_state(at, "current_question") is None 
    assert get_state(at, "current_page") is None
    assert_query_quiz(at, "nmr_quiz")
    assert "question" not in at.query_params or at.query_params.get("question") is None
    assert "page" not in at.query_params or at.query_params.get("page") is None
    assert_title(at, "titlenmr_quiz")

def test_url_direct_load_valid_question() -> None:
    """Test loading a valid question via URL query parameter."""
    at = AppTest.from_file("../../src/main.py")
    at.query_params["question"] = "ir_c_o_stretch_click"
    at.run()
    assert get_state(at, "current_question") == "ir_c_o_stretch_click"
    assert get_state(at, "navbar") == "IR"
    assert get_state(at, "current_page") is None
    assert get_state(at, "current_quiz") is None
    assert_title(at, "titleir_c_o_stretch_click")
    assert_query_question(at, "ir_c_o_stretch_click")
    assert "quiz" not in at.query_params or at.query_params.get("quiz") is None
    assert "page" not in at.query_params or at.query_params.get("page") is None

def test_url_direct_load_valid_quiz() -> None:
    """Test loading a valid quiz via URL query parameter."""
    at = AppTest.from_file("../../src/main.py")
    at.query_params["quiz"] = "nmr_quiz"
    at.run()
    assert get_state(at, "current_quiz") == "nmr_quiz"
    assert get_state(at, "navbar") == "NMR"
    assert get_state(at, "current_page") is None
    assert get_state(at, "current_question") is None
    assert_title(at, "titlenmr_quiz")
    assert_query_quiz(at, "nmr_quiz")
    assert "question" not in at.query_params or at.query_params.get("question") is None
    assert "page" not in at.query_params or at.query_params.get("page") is None


def test_multiple_question_navigations() -> None:
    """Test navigating through multiple question links."""
    at = run_app()

    click_button(at, "nmr_oxygen_shift_mcq")
    assert get_state(at, "current_question") == "nmr_oxygen_shift_mcq"
    assert get_state(at, "navbar") == "NMR"
    assert get_state(at, "current_page") is None
    assert get_state(at, "current_quiz") is None
    assert at.query_params.get("question") == ["nmr_oxygen_shift_mcq"]
    assert "quiz" not in at.query_params or at.query_params.get("quiz") is None
    assert "page" not in at.query_params or at.query_params.get("page") is None
    assert_title(at, "titlenmr_oxygen_shift_mcq")

    click_button(at, "ms_molecular_ion_mcq")
    assert get_state(at, "current_question") == "ms_molecular_ion_mcq"
    assert get_state(at, "navbar") == "MS"
    assert get_state(at, "current_page") is None
    assert get_state(at, "current_quiz") is None
    assert at.query_params.get("question") == ["ms_molecular_ion_mcq"]
    assert "quiz" not in at.query_params or at.query_params.get("quiz") is None
    assert "page" not in at.query_params or at.query_params.get("page") is None
    assert_title(at, "titlems_molecular_ion_mcq")

    click_button(at, "combo_unknown_a_mcq")
    assert get_state(at, "current_question") == "combo_unknown_a_mcq"
    assert get_state(at, "navbar") == "Combination exercises"
    assert get_state(at, "current_page") is None
    assert get_state(at, "current_quiz") is None
    assert at.query_params.get("question") == ["combo_unknown_a_mcq"]
    assert "quiz" not in at.query_params or at.query_params.get("quiz") is None
    assert "page" not in at.query_params or at.query_params.get("page") is None
    assert_title(at, "titlecombo_unknown_a_mcq")

def test_multiple_quiz_navigation() -> None:
    """Test navigating through multiple quiz links."""
    at = run_app()

    click_button(at, "quiz_nmr_quiz")
    assert get_state(at, "current_quiz") == "nmr_quiz"
    assert get_state(at, "navbar") == "NMR"
    assert get_state(at, "current_page") is None
    assert get_state(at, "current_question") is None
    assert_query_quiz(at, "nmr_quiz")
    assert "question" not in at.query_params or at.query_params.get("question") is None
    assert "page" not in at.query_params or at.query_params.get("page") is None
    assert_title(at, "titlenmr_quiz")

    click_button(at, "quiz_ir_quiz")
    assert get_state(at, "current_quiz") == "ir_quiz"
    assert get_state(at, "navbar") == "IR"
    assert get_state(at, "current_page") is None
    assert get_state(at, "current_question") is None
    assert_query_quiz(at, "ir_quiz")
    assert "question" not in at.query_params or at.query_params.get("question") is None
    assert "page" not in at.query_params or at.query_params.get("page") is None
    assert_title(at, "titleir_quiz")

def test_navigation_between_quizes_questions_pages() -> None:
    """Test navigation between quizes, questions and pages."""
    at = run_app()

    click_button(at, "quiz_nmr_quiz")
    assert get_state(at, "current_quiz") == "nmr_quiz"
    assert get_state(at, "navbar") == "NMR"
    assert get_state(at, "current_question") is None
    assert get_state(at, "current_page") is None
    assert "question" not in at.query_params or at.query_params.get("question") is None
    assert "page" not in at.query_params or at.query_params.get("page") is None
    assert_query_quiz(at, "nmr_quiz")
    assert_title(at, "titlenmr_quiz")

    click_button(at, "nmr_oxygen_shift_mcq")
    assert get_state(at, "current_question") == "nmr_oxygen_shift_mcq"
    assert get_state(at, "navbar") == "NMR"
    assert get_state(at, "current_quiz") is None
    assert get_state(at, "current_page") is None
    assert "quiz" not in at.query_params or at.query_params.get("quiz") is None
    assert "page" not in at.query_params or at.query_params.get("page") is None
    assert_query_question(at, "nmr_oxygen_shift_mcq")
    assert_title(at, "titlenmr_oxygen_shift_mcq")

    click_button(at, "Settings")
    assert get_state(at, "current_page") == "settings"
    assert get_state(at, "current_question") is None
    assert get_state(at, "current_quiz") is None
    assert get_state(at, "navbar") is None
    assert "question" not in at.query_params or at.query_params.get("question") is None
    assert "quiz" not in at.query_params or at.query_params.get("quiz") is None
    assert at.query_params.get("page") == ["settings"]
    assert_title(at, "Settings")

    click_button(at, "ir_c_o_stretch_click")
    assert get_state(at, "current_question") == "ir_c_o_stretch_click"
    assert get_state(at, "current_quiz") is None
    assert get_state(at, "current_page") is None
    assert get_state(at, "navbar") == "IR"
    assert at.query_params.get("question") == ["ir_c_o_stretch_click"]
    assert "quiz" not in at.query_params or at.query_params.get("quiz") is None
    assert "page" not in at.query_params or at.query_params.get("page") is None
    assert_title(at, "titleir_c_o_stretch_click")

    click_button(at, "Home")
    assert get_state(at, "current_page") == "home"
    assert get_state(at, "current_question") is None
    assert get_state(at, "current_quiz") is None
    assert get_state(at, "navbar") is None
    assert at.query_params.get("page") == ["home"]
    assert "question" not in at.query_params or at.query_params.get("question") is None
    assert "quiz" not in at.query_params or at.query_params.get("quiz") is None

def test_navigation_to_home() -> None:
    """Test navigation back to the home page."""
    at = run_app()

    at.sidebar.button("Home").click().run(timeout=10)

    assert len(at.exception) == 0
    assert get_state(at, "current_question") is None
    assert get_state(at, "current_page") == "home"
    assert get_state(at, "current_quiz") is None 
    assert get_state(at, "navbar") is None
    assert at.query_params.get("page") == ["home"] or at.query_params.get("page") is None
    assert "question" not in at.query_params or at.query_params.get("question") is None
    assert "quiz" not in at.query_params or at.query_params.get("quiz") is None


def test_navigation_to_settings() -> None:
    """Test navigation to the settings page."""
    at = click_button(run_app(), "Settings")

    assert get_state(at, "current_question") is None
    assert get_state(at, "current_page") == "settings"
    assert get_state(at, "current_quiz") is None 
    assert get_state(at, "navbar") is None
    assert at.query_params.get("page") == ["settings"]
    assert "question" not in at.query_params or at.query_params.get("question") is None
    assert "quiz" not in at.query_params or at.query_params.get("quiz") is None


def test_navigation_to_about() -> None:
    """Test navigation to the about page."""
    at = click_button(run_app(), "About")

    assert get_state(at, "current_question") is None
    assert get_state(at, "current_page") == "about"
    assert get_state(at, "current_quiz") is None 
    assert get_state(at, "navbar") is None
    assert at.query_params.get("page") == ["about"]
    assert "question" not in at.query_params or at.query_params.get("question") is None
    assert "quiz" not in at.query_params or at.query_params.get("quiz") is None
