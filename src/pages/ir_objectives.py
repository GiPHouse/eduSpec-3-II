import streamlit as st
from components.navigation import showNavbar, showIrSidebar

showNavbar()
st.title("IR Page")
st.write("Welcome to the IR Page!")
showIrSidebar()

