from IntegerQuestion import IntegerQuestion
from MultipleChoiceQuestion import MultipleChoiceQuestion
from QuestionDrawer import QuestionDrawer

questionint = IntegerQuestion(
    "title", "this is the body text", (10, 20), ["correct", "wrong too small", "wrong too big"]
)
# QuestionDrawer.drawQuestion(questionint)

questionmult = MultipleChoiceQuestion(
    "title", "this is the body text", ["10", "20", "30", "40"], 2, ["a", "b", "c", "d"]
)

QuestionDrawer.drawQuestion(questionmult)
