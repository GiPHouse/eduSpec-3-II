import streamlit as st

from components.navigation import showIrSidebar, showNavbar

showNavbar()
st.title("IR Page")
st.write("Welcome to the IR Page!")
showIrSidebar()

