from QuestionDrawer import QuestionDrawer
from SpectralQuestion import SpectralQuestion

spectralquest = SpectralQuestion(
    "id", "title", "this is the body text", "../spectra/easy001/ms.dx", 45.0, ["correct", "wrong"]
)

QuestionDrawer.drawQuestion(spectralquest)
