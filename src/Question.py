from abc import ABC, abstractmethod
from typing import *
class Question(ABC):

    def __init__(self, bodytext:str, imgpath:Optional[str]=None):

        self.bodytext = bodytext
        self.imgpath = imgpath

    @abstractmethod
    def verifyAndFeedback(self):
        pass

    @abstractmethod
    def feedback(self):
        pass
    