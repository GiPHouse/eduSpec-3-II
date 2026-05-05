import streamlit as st

from CustomThemes import showThemeSelector
from managers.QuizBuilder import QuizBuilder
from navigation import initPage


def homePage() -> None:
    """Shows the home page."""
    initPage()
    st.title("Welcome to the home page!")


def IRPage() -> None:
    """Shows the IR page."""
    initPage()
    st.title("Welcome to the IR page!")


def IRTheoryPage() -> None:
    """Shows the IR Theory page."""
    initPage()
    st.title("IR Theory")


def IRSpectralAreasPage() -> None:
    """Shows the IR Spectral Areas page."""
    initPage()
    st.title("IR Spectral Areas")


def IRSpectralAreaAPage() -> None:
    """Shows the IR Spectral Area A page."""
    initPage()
    st.title("Area A (3800 - 3200 cm-1)")


def IRSpectralAreaAQuizPage() -> None:
    """Shows the IR Spectral Area A Quiz page."""
    initPage()
    st.title("Mini Quiz Area A")


def IRSpectralAreaBPage() -> None:
    """Shows the IR Spectral Area B page."""
    initPage()
    st.title("Area B (3200 - 2700 cm-1)")


def IRSpectralAreaBQuizPage() -> None:
    """Shows the IR Spectral Area B Quiz page."""
    initPage()
    st.title("Mini Quiz Area B")


def IRSpectralAreaCPage() -> None:
    """Shows the IR Spectral Area C page."""
    initPage()
    st.title("Area C (2700 - 200 cm-1)")


def IRSpectralAreaCQuizPage() -> None:
    """Shows the IR Spectral Area C Quiz page."""
    initPage()
    st.title("Mini Quiz Area C")


def IRSpectralAreaDPage() -> None:
    """Shows the IR Spectral Area D page."""
    initPage()
    st.title("Area D (2000 - 1630 cm-1)")


def IRSpectralAreaDQuizPage() -> None:
    """Shows the IR Spectral Area D Quiz page."""
    initPage()
    st.title("Mini Quiz Area D")


def IRProteusQuizPage() -> None:
    """Shows the IR Proteus Quiz page."""
    initPage()
    st.title("Infrared Proteus Quiz")


def NMRPage() -> None:
    """Shows the NMR page."""
    initPage()
    st.title("Welcome to the NMR page!")


def HNMRTheoryPage() -> None:
    """Shows the H-NMR Theory page."""
    initPage()
    st.title("H-NMR Theory")


def CNMRTHeoryPage() -> None:
    """Shows the C-NMR Theory page."""
    initPage()
    st.title("CNMR Theory")


def MSPage() -> None:
    """Shows the MS page."""
    initPage()
    st.title("Mass spectrometry")


def CombinationExercisesPage() -> None:
    """Shows the Combination Exercises page."""
    initPage()
    st.title("Combination Exercises")
    q = QuizBuilder.buildQuiz(
        "quiz", ["question1", "question2", "question3", "question4", "question5"]
    )
    q.drawQuiz()


def UsingEduSpecPage() -> None:
    """Shows the using EduSpec page."""
    initPage()
    st.title("Using EduSpec")


def AboutPage() -> None:
    """Shows the about page."""
    initPage()
    st.title("About EduSpec")


def SettingsPage() -> None:
    """Shows the Settings page."""
    initPage()
    st.title("Settings")
    st.subheader("Theme")
    showThemeSelector()
