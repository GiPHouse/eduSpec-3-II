import streamlit as st

from src.pages.jsme_component import jsme_component

st.set_page_config(layout="wide")
st.title("JSME Component Test Harness")

seed = st.text_input("seed", "C", key="seed_input")
key = st.text_input("key", "jsme_test_1", key="key_input")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Editor")
    smiles = jsme_component(default_smiles=seed, key=key)

with col2:
    st.subheader("Returned SMILES")
    # This is what Selenium will assert on
    st.markdown(
        f'<div data-testid="returned-smiles">{smiles or ""}</div>',
        unsafe_allow_html=True,
    )

if st.button("Reset", key="reset_btn"):
    st.rerun()
