import json

from IntegerQuestion import IntegerQuestion
from MultipleChoiceQuestion import MultipleChoiceQuestion
from Question import Question
from WordQuestion import WordQuestion


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
        if not cls._verifyObject(obj):
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
                    imgpath=imgpath,
                )

            case "integer":
                bounds = (obj.get("lowerBound"), obj.get("upperBound"))
                feedbacks = obj.get("feedbacks")
                return IntegerQuestion(
                    name=name,
                    title=title,
                    bodytext=bodytext,
                    correct_answer=bounds,
                    feedbacks=feedbacks,
                    imgpath=imgpath,
                )

            case "word":
                correct_answer = obj.get("correctAnswer")
                feedbacks = [obj.get("correctFeedback"), obj.get("incorrectFeedback")]
                return WordQuestion(
                    name=name,
                    title=title,
                    bodytext=bodytext,
                    correct_answer=correct_answer,
                    feedbacks=feedbacks,
                    imgpath=imgpath,
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

            case "integer":
                # Integer questions must have an integer lower and higher bound, and 3 feedback options.
                # The lower bound must be lower than or equal to the higher bound
                lower_bound = obj.get("lowerBound")
                upper_bound = obj.get("upperBound")
                feedbacks = obj.get("feedbacks")
                if lower_bound is None or upper_bound is None or feedbacks is None:
                    return False
                if not isinstance(lower_bound, int) or not isinstance(upper_bound, int):
                    return False
                if lower_bound > upper_bound:
                    return False
                if len(feedbacks) != 3:
                    return False

            case "word":
                # Word questions must have a single correct answer string, a correct feedback and incorrect feedback
                correct_answer = obj.get("correctAnswer")
                correct_feedback = obj.get("correctFeedback")
                incorrect_feedback = obj.get("incorrectFeedback")
                if not correct_answer or not correct_feedback or not incorrect_feedback:
                    return False
                if not isinstance(correct_answer, str):
                    return False

            case n:
                raise TypeError(f"Attempted to verify unknown or illegal question type: {n}")

        return True
