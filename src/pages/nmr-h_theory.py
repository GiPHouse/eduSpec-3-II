import streamlit as st

from components.navigation import showNavbar, showNmrSidebar

showNavbar()
st.title("Theory")
st.write("NMR spectra come in very many different types, depending on the nuclei involved and the type of experiment that is carried out, but this section is limited to the interpretation of NMR spectra resulting from single pulse 1H (i.e. proton) experiments of liquid samples (including dissolved substances). Already this arguably simplest type of experiment leads to very information-rich spectra that can help you deduce the structure of many organic molecules. An example of the NMR spectrum of methyl isopropyl ketone is shown below.")
showNmrSidebar()

