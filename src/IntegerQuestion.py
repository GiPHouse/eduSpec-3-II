from Question import Question
from typing import *

class IntegerQuestion(Question):
    
    def __init__(self, title:str, bodytext:str, correct_answer:tuple[int,int], feedbacks:List[str],imgpath:Optional[str]=None):

        #the correct integer should be in the range between the first and second int, given as a tuple
        #feedbacks is as follows: [feedback for too small answer, feedback for right answer, feedback for too large answer]
        assert (correct_answer[0] <= correct_answer[1])
        assert(len(feedbacks) == 3)

        super().__init__(title,bodytext,imgpath)
        print(self.bodytext)
        self.correct_answer = correct_answer
        self.feedbacks = feedbacks


    def verifyAndFeedback(self, user_input:int):
        isAnswerCorrect:bool
        ReturnFeedback:str

        if user_input < self.correct_answer[0]:
            isAnswerCorrect = False
            ReturnFeedback = self.feedback(0)
        elif user_input > self.correct_answer[1]:
            isAnswerCorrect = False
            ReturnFeedback = self.feedback(2)
        else:
            isAnswerCorrect = True
            ReturnFeedback = self.feedback(1)
            
        return (isAnswerCorrect, ReturnFeedback)

    def feedback(self,input:int):
        return self.feedbacks[input]
    

