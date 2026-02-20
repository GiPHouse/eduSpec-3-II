import streamlit as st
from components.navigation import showNavbar, hideSidebar

showNavbar()
hideSidebar()
st.title("Welcome!")
st.write("Welcome to the Home Page!")