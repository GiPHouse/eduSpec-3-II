from MultipleChoiceQuestion import MultipleChoiceQuestion
from Question import Question

# st.write("""
# Hello world
# """)

mcq = MultipleChoiceQuestion("title", "hi", ["aaa", "bbb"], 0, ["true", "false"])
# QuestionDrawer.drawQuestion(mcq)
# print(type(mcq)==MultipleChoiceQuestion)
match mcq.__class__:
    case Question():
        print("Uh-oh")
    case MultipleChoiceQuestion():
        print("true")
    case n:
        print(n)
# mcq = MultipleChoiceQuestion("title","hi",["aaa","bbb"],0,["true","false"])
# QuestionDrawer.drawQuestion(mcq)
