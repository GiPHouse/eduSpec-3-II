from IntegerQuestion import IntegerQuestion
from QuestionDrawer import QuestionDrawer

questionint = IntegerQuestion(
    "tst",
    "title",
    "this is the body text",
    (10, 20),
    ["correct", "wrong too small", "wrong too big"],
    imgpath="../data/test.png",
)

QuestionDrawer.drawQuestion(questionint)
