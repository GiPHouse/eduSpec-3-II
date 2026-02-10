from Question import Question
from MultipleChoiceQuestion import MultipleChoiceQuestion
from IntegerQuestion import IntegerQuestion

class QuestionDrawer():
    
    @staticmethod
    def drawQuestion(current_question:Question):

        if current_question is MultipleChoiceQuestion:
            pass
        if current_question is IntegerQuestion:
            pass
        
