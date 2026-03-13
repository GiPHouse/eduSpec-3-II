import streamlit as st

from CustomThemes import THEMES, applyTheme, showThemeSelector
from managers.QuizBuilder import QuizBuilder


# Page functions
def homePage() -> None:
    """Shows the home page"""
    showNavbar()
    st.title("Welcome to the home page!")


def IRPage() -> None:
    """Shows the IR page"""
    showNavbar()
    createSidebar(IR_NAV)
    st.title("Welcome to the IR page!")


def IRTheoryPage() -> None:
    """Shows the IR Theory page"""
    showNavbar()
    createSidebar(IR_NAV)
    st.title("IR Theory")


def IRSpectralAreasPage() -> None:
    """Shows the IR Spectral Areas page"""
    showNavbar()
    createSidebar(IR_NAV)
    st.title("IR Spectral Areas")


def IRSpectralAreaAPage() -> None:
    """Shows the IR Spectral Area A page"""
    showNavbar()
    createSidebar(IR_NAV)
    st.title("Area A (3800 - 3200 cm-1)")


def IRSpectralAreaAQuizPage() -> None:
    """Shows the IR Spectral Area A Quiz page"""
    showNavbar()
    createSidebar(IR_NAV)
    st.title("Mini Quiz Area A")


def IRSpectralAreaBPage() -> None:
    """Shows the IR Spectral Area B page"""
    showNavbar()
    createSidebar(IR_NAV)
    st.title("Area B (3200 - 2700 cm-1)")


def IRSpectralAreaBQuizPage() -> None:
    """Shows the IR Spectral Area B Quiz page"""
    showNavbar()
    createSidebar(IR_NAV)
    st.title("Mini Quiz Area B")


def IRSpectralAreaCPage() -> None:
    """Shows the IR Spectral Area C page"""
    showNavbar()
    createSidebar(IR_NAV)
    st.title("Area C (2700 - 200 cm-1)")


def IRSpectralAreaCQuizPage() -> None:
    """Shows the IR Spectral Area C Quiz page"""
    showNavbar()
    createSidebar(IR_NAV)
    st.title("Mini Quiz Area C")


def IRSpectralAreaDPage() -> None:
    """Shows the IR Spectral Area D page"""
    showNavbar()
    createSidebar(IR_NAV)
    st.title("Area D (2000 - 1630 cm-1)")


def IRSpectralAreaDQuizPage() -> None:
    """Shows the IR Spectral Area D Quiz page"""
    showNavbar()
    createSidebar(IR_NAV)
    st.title("Mini Quiz Area D")


def IRProteusQuizPage() -> None:
    """Shows the IR Proteus Quiz page"""
    showNavbar()
    createSidebar(IR_NAV)
    st.title("Infrared Proteus Quiz")


def NMRPage() -> None:
    """Shows the NMR page"""
    showNavbar()
    createSidebar(NMR_NAV)
    st.title("Welcome to the NMR page!")


def HNMRTheoryPage() -> None:
    """Shows the H-NMR Theory page"""
    showNavbar()
    createSidebar(NMR_NAV)
    st.title("H-NMR Theory")


def CNMRTHeoryPage() -> None:
    """Shows the C-NMR Theory page"""
    showNavbar()
    createSidebar(NMR_NAV)
    st.title("CNMR Theory")


def MSPage() -> None:
    """Shows the MS page"""
    showNavbar()
    st.title("Mass spectrometry")


def CombinationExercisesPage() -> None:
    """Shows the Combination Exercises page"""
    showNavbar()
    st.title("Combination Exercises")
    q = QuizBuilder.buildQuiz(
        "quiz", ["question1", "question2", "question3", "question4", "question5"]
    )
    q.drawQuiz()


def UsingEduSpecPage() -> None:
    """Shows the using eduspec page"""
    showNavbar()
    st.title("Using EduSpec")


def AboutPage() -> None:
    """Shows the about page"""
    showNavbar()
    st.title("About EduSpec")


def SettingsPage() -> None:
    """Shows the Settings page"""
    showNavbar()
    st.title("Settings")
    st.subheader("Theme")
    showThemeSelector()


# Navigation session state
query_params = st.query_params

if "current_page" not in st.session_state:
    if "page" in query_params:
        st.session_state.current_page = query_params["page"]
    else:
        st.session_state.current_page = "Home"


def navigate(page: str) -> None:
    """Navigate to a different page

    Args:
        page (str): Name of the page you want to navigate to
    """
    st.session_state.current_page = page
    st.query_params["page"] = page  # update url
    st.rerun()


# Top navigation bar
def navbarButton(label: str, page: str) -> None:
    """Creates a button in the navigation bar at the top of the screen. The type of a button changes when the page is active.

    Args:
        label (str): The text that is shown on the button
        page (str): Name of the page you want to navigate to
    """
    type_button = "primary" if st.session_state.current_page == page else "tertiary"

    if st.button(label, type=type_button, key=page):
        navigate(page)


def showNavbar() -> None:
    """Displays the navigation bar that is at the top of the page."""
    if "theme" not in st.session_state:
        st.session_state["theme"] = "Light"
    applyTheme(THEMES[st.session_state["theme"]])

    cols = st.columns([1.5, 1, 1.3, 1.25, 2.3, 2, 1.5, 1.75])
    with cols[0]:
        navbarButton("Home", "Home")
    with cols[1]:
        navbarButton("IR", "IR")
    with cols[2]:
        navbarButton("NMR", "NMR")
    with cols[3]:
        navbarButton("MS", "MS")
    with cols[4]:
        navbarButton("Combination Exercises", "Combination Exercises")
    with cols[5]:
        navbarButton("Using Eduspec", "Using EduSpec")
    with cols[6]:
        navbarButton("About", "About")
    with cols[7]:
        navbarButton("Setting", "Setting")


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


IR_NAV = [
    {
        "title": "Infrared Spectroscopy",
        "items": [
            {"label": "Theory", "page": "IR Theory"},
            {
                "label": "Spectral Areas",
                "page": "IR Spectral Areas",
                "children": [
                    {
                        "label": "Area A (3800–3200 cm-1)",
                        "page": "IR Area A",
                        "children": [{"label": "Mini Quiz", "page": "IR Area A Quiz"}],
                    },
                    {
                        "label": "Area B (3200–2700 cm-1)",
                        "page": "IR Area B",
                        "children": [{"label": "Mini Quiz", "page": "IR Area B Quiz"}],
                    },
                    {
                        "label": "Area C (2700–2000 cm-1)",
                        "page": "IR Area C",
                        "children": [{"label": "Mini Quiz", "page": "IR Area C Quiz"}],
                    },
                    {
                        "label": "Area D (2000–1630 cm-1)",
                        "page": "IR Area D",
                        "children": [{"label": "Mini Quiz", "page": "IR Area D Quiz"}],
                    },
                ],
            },
            {"label": "Infrared Proteus Quiz", "page": "IR Proteus Quiz"},
        ],
    },
]

NMR_NAV = [
    {
        "title": "¹H-NMR Spectroscopy",
        "items": [{"label": "Theory", "page": "H-NMR Theory"}],
    },
    {
        "title": "¹³C-NMR Spectroscopy",
        "items": [{"label": "Theory", "page": "C-NMR Theory"}],
    },
]


PAGES = {
    "Home": homePage,
    "IR": IRPage,
    "IR Theory": IRTheoryPage,
    "IR Spectral Areas": IRSpectralAreasPage,
    "IR Area A": IRSpectralAreaAPage,
    "IR Area A Quiz": IRSpectralAreaAQuizPage,
    "IR Area B": IRSpectralAreaBPage,
    "IR Area B Quiz": IRSpectralAreaBQuizPage,
    "IR Area C": IRSpectralAreaCPage,
    "IR Area C Quiz": IRSpectralAreaCQuizPage,
    "IR Area D": IRSpectralAreaDPage,
    "IR Area D Quiz": IRSpectralAreaDQuizPage,
    "IR Proteus Quiz": IRProteusQuizPage,
    "NMR": NMRPage,
    "H-NMR Theory": HNMRTheoryPage,
    "C-NMR Theory": CNMRTHeoryPage,
    "MS": MSPage,
    "Combination Exercises": CombinationExercisesPage,
    "Using EduSpec": UsingEduSpecPage,
    "About": AboutPage,
    "Setting": SettingsPage,  # Add this
}

current_page = st.session_state.current_page
page_function = PAGES[current_page]
page_function()
