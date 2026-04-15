import json
from pathlib import Path

import streamlit as st

from CustomThemes import THEMES, applyTheme, showThemeSelector
from managers.QuizBuilder import QuizBuilder
from navigation import createSidebar, initPage

# Get the absolute path to the data directory
data_dir = Path(__file__).parent.parent / "data"

#load the sidebars from json
with open(data_dir / "navigation" / "ir_sidebar.json", 'r') as file:
    IR_NAV = json.load(file)

with open(data_dir / "navigation" / "nmr_sidebar.json", 'r') as file:
    NMR_NAV = json.load(file)

# Page functions
def homePage() -> None:
    """Shows the home page"""
    initPage()
    st.title("Welcome to the home page!")


def IRPage() -> None:
    """Shows the IR page"""
    initPage()
    createSidebar(IR_NAV)
    st.title("Welcome to the IR page!")


def IRTheoryPage() -> None:
    """Shows the IR Theory page"""
    initPage()
    createSidebar(IR_NAV)
    st.title("IR Theory")


def IRSpectralAreasPage() -> None:
    """Shows the IR Spectral Areas page"""
    initPage()
    createSidebar(IR_NAV)
    st.title("IR Spectral Areas")


def IRSpectralAreaAPage() -> None:
    """Shows the IR Spectral Area A page"""
    initPage()
    createSidebar(IR_NAV)
    st.title("Area A (3800 - 3200 cm-1)")


def IRSpectralAreaAQuizPage() -> None:
    """Shows the IR Spectral Area A Quiz page"""
    initPage()
    createSidebar(IR_NAV)
    st.title("Mini Quiz Area A")


def IRSpectralAreaBPage() -> None:
    """Shows the IR Spectral Area B page"""
    initPage()
    createSidebar(IR_NAV)
    st.title("Area B (3200 - 2700 cm-1)")


def IRSpectralAreaBQuizPage() -> None:
    """Shows the IR Spectral Area B Quiz page"""
    initPage()
    createSidebar(IR_NAV)
    st.title("Mini Quiz Area B")


def IRSpectralAreaCPage() -> None:
    """Shows the IR Spectral Area C page"""
    initPage()
    createSidebar(IR_NAV)
    st.title("Area C (2700 - 200 cm-1)")


def IRSpectralAreaCQuizPage() -> None:
    """Shows the IR Spectral Area C Quiz page"""
    initPage()
    createSidebar(IR_NAV)
    st.title("Mini Quiz Area C")


def IRSpectralAreaDPage() -> None:
    """Shows the IR Spectral Area D page"""
    initPage()
    createSidebar(IR_NAV)
    st.title("Area D (2000 - 1630 cm-1)")


def IRSpectralAreaDQuizPage() -> None:
    """Shows the IR Spectral Area D Quiz page"""
    initPage()
    createSidebar(IR_NAV)
    st.title("Mini Quiz Area D")


def IRProteusQuizPage() -> None:
    """Shows the IR Proteus Quiz page"""
    initPage()
    createSidebar(IR_NAV)
    st.title("Infrared Proteus Quiz")


def NMRPage() -> None:
    """Shows the NMR page"""
    initPage()
    createSidebar(NMR_NAV)
    st.title("Welcome to the NMR page!")


def HNMRTheoryPage() -> None:
    """Shows the H-NMR Theory page"""
    initPage()
    createSidebar(NMR_NAV)
    st.title("H-NMR Theory")


def CNMRTHeoryPage() -> None:
    """Shows the C-NMR Theory page"""
    initPage()
    createSidebar(NMR_NAV)
    st.title("CNMR Theory")


def MSPage() -> None:
    """Shows the MS page"""
    initPage()
    st.title("Mass spectrometry")


def CombinationExercisesPage() -> None:
    """Shows the Combination Exercises page"""
    initPage()
    st.title("Combination Exercises")
    q = QuizBuilder.buildQuiz(
        "quiz", ["question1", "question2", "question3", "question4", "question5"]
    )
    q.drawQuiz()


def UsingEduSpecPage() -> None:
    """Shows the using eduspec page"""
    initPage()
    st.title("Using EduSpec")


def AboutPage() -> None:
    """Shows the about page"""
    initPage()
    st.title("About EduSpec")


def SettingsPage() -> None:
    """Shows the Settings page"""
    initPage()
    st.title("Settings")
    st.subheader("Theme")
    showThemeSelector()
