import streamlit as st

def initCurrentPageSessionState():
    """Initializes the session state for the current page
    """
    if "current_page" not in st.session_state:
        st.session_state.current_page = "pages/home.py"

def navbarButton(label: str, page: str):
    """Creates a button in the navigation bar at the top of the screen.
    The type of a button changes when the page is active.

    Args:
        label (str): The text that is shown on the button
        page (str): The relative path to the page to navigate to when the button is pressed.
    """
    type_button = "primary" if st.session_state.current_page == page else "secondary"

    if st.button(label, type=type_button):
        st.session_state.current_page = page
        st.switch_page(page)

def showNavbar():
    """ Displays the navigation bar that is at the top of the page.
    Returns: None
    """
    initCurrentPageSessionState()
    cols = st.columns([1.5, 1, 1.25, 1, 2, 2, 2])
    with cols[0]:
        navbarButton("Home", "pages/home.py")
    with cols[1]:
        navbarButton("IR", "pages/ir_objectives.py")
    with cols[2]:
        navbarButton("NMR", "pages/nmr_objectives.py")
    with cols[3]:
        navbarButton("MS", "pages/ms_objectives.py")
    with cols[4]:
        navbarButton("Combination Exercises", "pages/combination_exercises.py")
    with cols[5]:
        navbarButton("Using Eduspec", "pages/using_eduspec.py")
    with cols[6]:
        navbarButton("About", "pages/about.py")

def hideSidebar():
    """Hides the entire sidebar that streamlit automatically makes.
    Returns: None
    """
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

def removePagesSidebar():
    """Removes the pages in the sidebar that Streamlit automatically adds to the sidebar.
    Streamlit automatically adds the pages in the folder /pages to the sidebar navigation.
    Returns: None
    """
    st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

def sidebar_button(label:str, page:str, indent:int):
    """Creates a button (with indentation) that is shown in the sidebar.
    The button is used for navigation between pages.
    The type of the button changes when the page is active.
    
    Args:
        label (str): Text that is shown on the button
        page (str): The relative path to the page to navigate to when the button is pressed.
        indent (int): Indentation level of the button. Higher value increase the left spacing.
    Returns:
        None
    """

    type_button = "primary" if st.session_state.current_page == page else "secondary"

    if indent > 0:
        cols = st.sidebar.columns([indent, 20])
        with cols[1]:
            if st.button(label, type=type_button):
                st.session_state.current_page = page
                st.switch_page(page)
    else:
        if st.sidebar.button(label, type=type_button):
            st.session_state.current_page = page
            st.switch_page(page)

def showIrSidebar():
    """Shows the navigation in the sidebar that is on the IR pages.
    The navigation menu expands (shows extra navigation buttons) for certained pages.

    Returns:
        None
    """
    removePagesSidebar()
    initCurrentPageSessionState()
    # Expand submenu for certained pages.
    spectral_expanded = st.session_state.current_page in [
        "pages/ir_spectral_areas.py",
        "pages/ir_spectral_area_a.py",
        "pages/ir_spectral_area_a_quiz.py",
        "pages/ir_spectral_area_b.py",
        "pages/ir_spectral_area_b_quiz.py",
        "pages/ir_spectral_area_c.py",
        "pages/ir_spectral_area_c_quiz.py",
        "pages/ir_spectral_area_d.py",
        "pages/ir_spectral_area_d_quiz.py",
    ]

    st.sidebar.title("Infrared Spectroscopy")
    sidebar_button("Theory", "pages/ir_theory.py", 0)
    sidebar_button("Spectral Areas", "pages/ir_spectral_areas.py", 0)
    # Expanded submenu
    if spectral_expanded:
        sidebar_button("Area A (3800 - 3200 cm-1)", "pages/ir_spectral_area_a.py", 1)
        if st.session_state.current_page == "pages/ir_spectral_area_a.py" or st.session_state.current_page == "pages/ir_spectral_area_a_quiz.py":
            sidebar_button("Mini Quiz", "pages/ir_spectral_area_a_quiz.py", 2)
        sidebar_button("Area B (3200 - 2700 cm-1)", "pages/ir_spectral_area_b.py", 1)
        if st.session_state.current_page == "pages/ir_spectral_area_b.py" or st.session_state.current_page == "pages/ir_spectral_area_b_quiz.py":
            sidebar_button("Mini Quiz", "pages/ir_spectral_area_b_quiz.py", 2)
        sidebar_button("Area C (2700 - 2000 cm-1)", "pages/ir_spectral_area_c.py", 1)
        if st.session_state.current_page == "pages/ir_spectral_area_c.py" or st.session_state.current_page == "pages/ir_spectral_area_c_quiz.py":
            sidebar_button("Mini Quiz", "pages/ir_spectral_area_c_quiz.py", 2)
        sidebar_button("Area D (2000 - 1630 cm-1)", "pages/ir_spectral_area_d.py", 1)
        if st.session_state.current_page == "pages/ir_spectral_area_d.py" or st.session_state.current_page == "pages/ir_spectral_area_d_quiz.py":
            sidebar_button("Mini Quiz", "pages/ir_spectral_area_d_quiz.py", 2)
    sidebar_button("Infrared Proteus Quiz", "pages/ir_proteus_quiz.py", 0)

def showNmrSidebar(current_page:str=None):
    removePagesSidebar()
    st.sidebar.title("¹H-NMR Spectroscopy")
    sidebar_button("Theory", "pages/nmr-h_theory.py", 0)
    st.sidebar.title("¹³C-NMR Spectroscopy")
    st.sidebar.title("2D NMR Spectroscopy")