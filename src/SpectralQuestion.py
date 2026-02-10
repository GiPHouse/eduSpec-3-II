from Question import Question
from typing import *

class SpectralQuestion(Question):
    
    def __init__(self, title:str, bodytext:str,imgpath:Optional[str]=None):
        super().__init__(title,bodytext,imgpath)
    def verifyAndFeedback(self, user_input:int):
        pass
    def feedbsck(user_input:int):
        pass