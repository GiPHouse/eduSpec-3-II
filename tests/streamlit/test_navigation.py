from streamlit.testing.v1 import AppTest


def click_button(at: AppTest, label: str) -> AppTest:
    """Click the first button with the matching label."""
    next(button for button in at.button if button.label == label).click()
    return at.run()


def test_top_level_navigation_updates_url() -> None:
    """Top-level pages are reachable through the sidebar tab content."""
    at = AppTest.from_file("../../src/navigation.py")
    at.run()

    click_button(at, "Open IR Overview")
    assert at.session_state["current_page"] == "IR"
    assert at.query_params["page"] == ["IR"]

    click_button(at, "Open Mass Overview")
    assert at.session_state["current_page"] == "Mass"
    assert at.query_params["page"] == ["Mass"]


def test_nested_navigation_updates_url() -> None:
    """Nested expander buttons navigate to section, quiz, and question pages."""
    at = AppTest.from_file("../../src/navigation.py")
    at.run()

    click_button(at, "Open Spectral Areas")
    assert at.session_state["current_page"] == "IR Spectral Areas"
    assert at.query_params["page"] == ["IR Spectral Areas"]

    click_button(at, "Open Area A")
    assert at.session_state["current_page"] == "IR Area A"
    assert at.query_params["page"] == ["IR Area A"]

    click_button(at, "Area A Quiz")
    assert at.session_state["current_page"] == "IR Area A Quiz"
    assert at.query_params["page"] == ["IR Area A Quiz"]


def test_url_direct_load() -> None:
    """The page state is restored directly from the URL."""
    at = AppTest.from_file("../../src/navigation.py")
    at.query_params["page"] = ["IR Area B"]
    at.run()

    assert at.session_state["current_page"] == "IR Area B"
