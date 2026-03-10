from streamlit.testing.v1 import AppTest


def test_navbar_navigation() -> None:
    """Test for the top navigation bar."""
    at = AppTest.from_file("../navigation.py")
    at.run()

    at.button("IR").click().run()  # Click IR button
    assert at.session_state["current_page"] == "IR"
    assert at.query_params["page"] == ["IR"]

    at.button("About").click().run()  # Click About button
    assert at.session_state["current_page"] == "About"
    assert at.query_params["page"] == ["About"]


def test_sidebar_navigation() -> None:
    """Test for the sidebar navigation"""
    at = AppTest.from_file("../navigation.py")
    at.run()

    at.button("IR").click().run()  # Click IR button
    at.button("IR Spectral Areas").click().run()  # Click IR Spectral Areas button in the sidebar
    assert at.session_state["current_page"] == "IR Spectral Areas"
    assert at.query_params["page"] == ["IR Spectral Areas"]

    at.button("IR Area A").click().run()  # Click Area A button
    assert at.session_state["current_page"] == "IR Area A"
    assert at.query_params["page"] == ["IR Area A"]

    at.button("IR Area A Quiz").click().run()  # Click Mini Quiz button
    assert at.session_state["current_page"] == "IR Area A Quiz"
    assert at.query_params["page"] == ["IR Area A Quiz"]


def test_url_direct_load() -> None:
    """Test when the url is loaded"""
    at = AppTest.from_file("../navigation.py")
    at.query_params["page"] = ["IR Area B"]
    at.run()
    assert at.session_state["current_page"] == "IR Area B"
