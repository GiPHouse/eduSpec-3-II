import pathlib

from QuestionBuilder import QuestionBuilder
from Quiz import Quiz


class QuizBuilder:
    """A class to create a quiz object from question id's, by parsing the corresponding JSON files"""

    @staticmethod
    def buildQuiz(name: str, id_list: list[str]) -> Quiz:
        """_summary_

        Args:
            name (str): _description_
            id_list (list[str]): _description_

        Returns:
            Quiz: _description_
        """
        question_path = str(pathlib.Path(__file__).parent.parent.resolve()) + "/questions/"
        question_list = []

        for i in id_list:
            with open(question_path + i + ".json", "r", encoding="utf-8") as file:
                json_string = file.read()
                question_list.append(QuestionBuilder.questionFromJson(json_string))

        return Quiz(name, question_list)
