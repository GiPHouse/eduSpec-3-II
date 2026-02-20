import streamlit as st

from components.navigation import hideSidebar, showNavbar

showNavbar()
hideSidebar()
st.title("Welcome!")
st.write("Welcome to the Home Page!")