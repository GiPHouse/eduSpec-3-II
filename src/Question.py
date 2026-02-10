from abc import ABC, abstractmethod
from typing import *
class Question(ABC):

    def __init__(self, title:str, bodytext:str, imgpath:Optional[str]=None):

        self.bodytext = bodytext
        self.imgpath = imgpath
        self.title  =title

    @abstractmethod
    def verifyAndFeedback(self):
        pass

    @abstractmethod
    def feedback(self):
        pass
    