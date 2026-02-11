from Question import Question
from typing import *
import numpy as np
import plotly.graph_objects as go
import jcamp

class SpectralQuestion(Question):
    
    def __init__(self, title:str, bodytext:str,imgpath:Optional[str]):
        super().__init__(title,bodytext,imgpath)
    def verifyAndFeedback(self, user_input:int):
        pass
    def feedback(user_input:int):
        pass


    def parse_jcampdx(self):
        """
        Parsing logic for JCAMP-DX files.
        Returns x and y dimensions of the parsed data.
        """

        with open(self.imgpath, "rb") as f:
            lines = [ln.decode("utf-8", errors="replace") for ln in f.read().splitlines()]

        data = jcamp.jcamp_read(lines)

        x = np.asarray(data["x"], dtype=float)
        y = np.asarray(data["y"], dtype=float)

        if y.max() > 0:
            y = (y / y.max()) * 100
        self.units=data.get("xunits", "m/z")



        return (x,y)