import streamlit as st
from components.navigation import showNavbar, showIrSidebar

showNavbar()
st.title("Spectral Areas")
st.write("Welcome to the IR Spectral Areas Page!")
showIrSidebar()