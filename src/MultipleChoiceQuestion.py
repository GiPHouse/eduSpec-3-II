from Question import Question
from typing import *

class MultipleChoiceQuestion(Question):
    
    def __init__(self, bodytext:str, answers:List[str], correct_answer:int, feedbacks:List[str],imgpath:Optional[str]=None):

        assert (len(answers) == len(feedbacks))
        assert (correct_answer >=0 and correct_answer<len(answers))

        super().__init__(bodytext,imgpath)
        print(self.bodytext)
        self.answers = answers
        self.correct_answer = correct_answer
        self.feedbacks = feedbacks


    def verifyAndFeedback(self, user_input:int):
        return ((self.correct_answer == user_input), self.feedback(user_input))

    def feedback(self,user_input):
        return self.feedbacks[user_input]
    

