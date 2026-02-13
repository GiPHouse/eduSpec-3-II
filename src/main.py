from MultipleChoiceQuestion import MultipleChoiceQuestion
from Question import Question
from QuestionSerialiser import QuestionSerialiser

# st.write("""
# Hello world
# """)

mcq = MultipleChoiceQuestion("question1", "title", "hi", ["aaa", "bbb"], 0, ["true", "false"])
# mcq = MultipleChoiceQuestion("title", "hi", ["aaa", "bbb"], 0, ["true", "false"])
# QuestionDrawer.drawQuestion(mcq)
# print(type(mcq)==MultipleChoiceQuestion)
match mcq.__class__:
    case Question():
        print("Uh-oh")
    case MultipleChoiceQuestion():
        print("true")
    case n:
        print(n)
# QuestionDrawer.drawQuestion(mcq)
print(QuestionSerialiser.questionToJson(mcq))
