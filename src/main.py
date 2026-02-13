import streamlit as st

from QuestionDrawer import QuestionDrawer
from SpectralQuestion import SpectralQuestion

st.write("""
Hello world
""")

# mcq = MultipleChoiceQuestion("title","hi",["aaa","bbb"],0,["true","false"])
# QuestionDrawer.drawQuestion(mcq)

spc = SpectralQuestion("title", "bodytext", "../spectra/easy001/ir.dx")
figure = QuestionDrawer.drawQuestion(spc)
# The Question Drawer should actually return the figure and a button, something for us to figure out.

if figure is not None:
    st.plotly_chart(figure, use_container_width=True)
else:
    st.warning("No figure returned for this question type.")
