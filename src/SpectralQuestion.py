from Question import Question
from typing import *

class SpectralQuestion(Question):
     def __init__(self, title:str, bodytext:str,imgpath:Optional[str]=None):
           super().__init__(bodytext,imgpath)
     
