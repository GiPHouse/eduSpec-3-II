import json

from MultipleChoiceQuestion import MultipleChoiceQuestion
from Question import Question


class QuestionBuilder:
    """Builder class for all question types.

    This will take in json and generate a question instance.
    """

    @classmethod
    def questionFromJson(cls, data: str) -> Question:
        """Builds a question from json data.

        Will only work with correct data, otherwise it'll raise errors.

        Args:
            data (str): The json string describing the question.

        Raises:
            TypeError: When encountering an unrecognised question type.
            ValueError: When encountering a malformed question.

        Returns:
            Question: The built question. This can be any question subtype, but will never be the interface/parent `Question` class.
        """
        obj = json.loads(data)
        if not cls.verifyJson(data):
            raise ValueError(f"Failed verifying {obj.get('type')} {obj.get('id')}.")

        question_type = obj.get("type")
        obj.get("version")
        name = obj.get("id")
        title = obj.get("title")
        bodytext = obj.get("bodyText")
        imgpath = obj.get("imagePath")
        if len(imgpath) == 0:
            imgpath = None

        match question_type:
            case "multipleChoice":
                answers = obj.get("answers")
                feedbacks = obj.get("feedbacks")
                correct_answer = obj.get("correctAnswer")
                return MultipleChoiceQuestion(
                    name=name,
                    title=title,
                    bodytext=bodytext,
                    answers=answers,
                    feedbacks=feedbacks,
                    correct_answer=correct_answer,
                )
            case n:
                raise TypeError(f"Attempted to build unknown or illegal question type: {n}")

    @classmethod
    def verifyJson(cls, data: str) -> bool:
        """Verifies whether the json string of a question can be used to generate a question.

        Args:
            data (str): Json string describing a question.

        Raises:
            TypeError: When encountering an unrecognised question type.

        Returns:
            bool: Whether the data is formatted correctly.
        """
        obj = json.loads(data)
        return cls._verifyObject(obj)

    @classmethod
    def _verifyObject(cls, obj: dict) -> bool:
        """Verifies loaded json object. Internal use only, use `verifyJson` otherwise.

        Args:
            obj (dict): The deserialised dict.

        Raises:
            TypeError: When encountering an unrecognised question type.

        Returns:
            bool: Whether the object is formatted correctly.
        """
        """
        Shared fields:
        - id (string): The question id/name
        - title (string): The question title
        - bodyText (string): The question body text
        - imagePath (string): The image path. Empty if None
        - version (int): The version of that specific serialiser
        - type (str): The type of question
        """

        # Testing whether each basic attribute exists and isn't empty/zero
        for attr in ("id", "title", "bodyText", "version", "type"):
            # Non-empty strings and non-zero integers are True in Python
            if not obj.get(attr, None):
                return False

        if obj.get("imagePath") is None:
            return False

        # Test any questiontype-specific attributes
        match obj.get("type"):
            case "multipleChoice":
                # Multiple-choice questions must have at least 2 answers, the same amount of feedbacks, and a valid correct answer
                answers = obj.get("answers")
                feedbacks = obj.get("feedbacks")
                correct_answer = obj.get("correctAnswer")
                if not answers or not feedbacks or not correct_answer:
                    return False
                if len(answers) < 2:
                    return False
                if len(feedbacks) != len(answers):
                    return False
                if correct_answer < 0 or correct_answer >= len(answers):
                    return False

            case n:
                raise TypeError(f"Attempted to build unknown or illegal question type: {n}")

        return True
