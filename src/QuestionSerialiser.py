import json

from MultipleChoiceQuestion import MultipleChoiceQuestion
from Question import Question


class QuestionSerialiser:
    """Class to convert any question to JSON"""

    @classmethod
    def questionToJson(cls, question: Question) -> str:
        """Converts any question to JSON. Do not use the parent `Question` class.

        Args:
            question (Question): The question to convert

        Raises:
            ValueError: Raises a ValueError on an unrecognised question type (this includes the parent `Question` class)

        Returns:
            str: The generated JSON
        """
        match question:
            case MultipleChoiceQuestion():
                return cls._convertMultipleChoiceQuestion(question)
            case n:
                raise TypeError(f"Unknown or illegal question type encountered: {n.__class__}")

    @classmethod
    def _convertMultipleChoiceQuestion(cls, question: MultipleChoiceQuestion) -> str:
        """Serialises a MultipleChoiceQuestion to JSON

        Args:
            question (MultipleChoiceQuestion): The multiple-choice question to convert

        Returns:
            str: The generated JSON

            The JSON has the following template:
            - id (string): The question id
            - version (number): The saved version
            - type (string) "multipleChoice": The question type
            - title (string): The question title
            - bodyText (string): The question body text
            - imagePath (string): The image path. Empty if None
            - answers (array): The possible answers
            - correctAnswer (number): The correct answer as index of answers
            - feedbacks (array): The feedbacks given at each answer
            -
        """
        data_out = cls._buildGenericQuestion(question)

        # ! Version number is hardcoded and updated when editing this function or _buildGenericQuestion
        data_out["version"] = 1
        data_out["type"] = "multipleChoice"

        data_out["answers"] = question.answers
        data_out["correctAnswer"] = question.correct_answer
        data_out["feedbacks"] = question.feedbacks

        return json.dumps(data_out)

    @classmethod
    def _buildGenericQuestion(cls, question: Question) -> dict:
        """Creates a base dictionary for all questions to work off

        Args:
            question (Question): The question to convert

        Returns:
            dict: A dictionary with the shared attributes ready for serialisation

            The dict includes the following values:
            - id (string): The question id/name
            - title (string): The question title
            - bodyText (string): The question body text
            - imagePath (string): The image path. Empty if None
        """
        # ! Versioning is done in the individual functions. When updating this function, increase all by 100
        data_out = {}

        data_out["id"] = question.name
        data_out["title"] = question.title
        data_out["bodyText"] = question.bodytext

        imagepath = question.imgpath
        if imagepath is None:
            data_out["imagePath"] = ""
        else:
            data_out["imagePath"] = imagepath

        return data_out
