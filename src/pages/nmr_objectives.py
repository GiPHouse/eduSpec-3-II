import streamlit as st
from components.navigation import showNavbar, showNmrSidebar

showNavbar()
st.title("NMR")
st.write("Welcome to the NMR Page!")
showNmrSidebar()

