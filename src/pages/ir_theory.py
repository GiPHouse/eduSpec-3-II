import streamlit as st
from components.navigation import showNavbar, showIrSidebar

showNavbar()
st.title("Infrared Spectroscopy \n Theory")
st.write("Welcome to the IR Theory Page!")
showIrSidebar()
