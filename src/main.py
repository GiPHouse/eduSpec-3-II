from QuestionDrawer import QuestionDrawer
from questions.MoleculeDrawingQuestion import MoleculeDrawingConfig, MoleculeDrawingQuestion

q = MoleculeDrawingQuestion(
    name="",
    title="Draw ethanol",
    bodytext="Use the editor to draw ethanol and submit.",
    config=MoleculeDrawingConfig(
        expected_smiles="CCO",
        seed_smiles="",
        widget_key="q1",
    ),
)

QuestionDrawer.drawQuestion(q)


# QuestionDrawer.drawQuestion(questionmult)
