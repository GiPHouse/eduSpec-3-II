import streamlit as st
from components.navigation import showNavbar, showIrSidebar

showNavbar()
st.title("Infrared Proteus Quiz")
st.write("Welcome to the Infrared Proteus Quiz Page!")
showIrSidebar()