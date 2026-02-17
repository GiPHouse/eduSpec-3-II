from IntegerQuestion import IntegerQuestion
from QuestionDrawer import QuestionDrawer

question = IntegerQuestion(
    "title", "this is the body text", (10, 20), ["correct", "wrong too small", "wrong too big"]
)
QuestionDrawer.drawQuestion(question)
