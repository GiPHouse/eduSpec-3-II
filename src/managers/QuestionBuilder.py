import json

from questions.IntegerQuestion import IntegerQuestion
from questions.MoleculeDrawingQuestion import MoleculeDrawingConfig, MoleculeDrawingQuestion
from questions.MultipleChoiceQuestion import MultipleChoiceQuestion
from questions.Question import Question
from questions.SpectralQuestion import SpectralQuestion
from questions.WordQuestion import WordQuestion


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
        body_format = obj.get("bodyFormat", "text")
        figures = obj.get("figures")
        spectralpath = obj.get("spectralpath")

        match question_type:
            case "multipleChoice":
                answers = obj.get("answers")
                feedbacks = obj.get("feedbacks")
                correct_answer = obj.get("correctAnswer")
                return MultipleChoiceQuestion(
                    name=name,
                    title=title,
                    bodytext=bodytext,
                    body_format=body_format,
                    answers=answers,
                    feedbacks=feedbacks,
                    correct_answer=correct_answer,
                    figures=figures,
                )

            case "integer":
                bounds = (obj.get("lowerBound"), obj.get("upperBound"))
                feedbacks = obj.get("feedbacks")
                return IntegerQuestion(
                    name=name,
                    title=title,
                    bodytext=bodytext,
                    body_format=body_format,
                    correct_answer=bounds,
                    feedbacks=feedbacks,
                    figures=figures,
                )

            case "word":
                correct_answer = obj.get("correctAnswer")
                feedbacks = [obj.get("correctFeedback"), obj.get("incorrectFeedback")]
                return WordQuestion(
                    name=name,
                    title=title,
                    bodytext=bodytext,
                    body_format=body_format,
                    correct_answer=correct_answer,
                    feedbacks=feedbacks,
                    figures=figures,
                )

            case "spectral":
                correct_answer = obj.get("correctAnswer")
                feedbacks = obj.get("feedbacks")
                tolerance = obj.get("tolerance")

                return SpectralQuestion(
                    name=name,
                    title=title,
                    bodytext=bodytext,
                    body_format=body_format,
                    correct_answer=float(correct_answer),
                    feedbacks=feedbacks,
                    figures=figures,
                    spectralpath=spectralpath,
                    tolerance=float(tolerance),
                )

            case "drawing":
                feedbacks = [obj.get("correctFeedback"), obj.get("incorrectFeedback")]
                correct_answer = obj.get("correctAnswer")
                default_answer = obj.get("defaultAnswer")
                widget_key = obj.get("widgetKey")
                config = MoleculeDrawingConfig(
                    expected_smiles=correct_answer,
                    seed_smiles=default_answer,
                    widget_key=widget_key,
                )

                return MoleculeDrawingQuestion(
                    name=name,
                    title=title,
                    bodytext=bodytext,
                    body_format=body_format,
                    config=config,
                    feedbacks=feedbacks,
                    figures=figures,
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
        - bodyFormat (string): The format of question body test
        - figures (string): The image path. Empty if None
        - version (int): The version of that specific serialiser
        - type (str): The type of question
        """

        # Testing whether each basic attribute exists and isn't empty/zero
        for attr in ("id", "title", "bodyText", "version", "type"):
            # Non-empty strings and non-zero integers are True in Python
            if not obj.get(attr, None):
                return False
        body_format = obj.get("bodyFormat", "text")
        if body_format not in ("text", "latex"):
            return False

        if obj.get("figures") is None:
            return False

        # Test any questiontype-specific attributes
        match obj.get("type"):
            case "multipleChoice":
                # Multiple-choice questions must have at least 2 answers, the same amount of feedbacks, and a valid correct answer
                answers = obj.get("answers")
                feedbacks = obj.get("feedbacks")
                correct_answer = obj.get("correctAnswer")
                if not answers or not feedbacks:
                    return False
                if correct_answer is None or not isinstance(correct_answer, int):
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
                if not isinstance(lower_bound, (int, float)) or not isinstance(
                    upper_bound, (int, float)
                ):
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

            case "spectral":
                # A single correct answer (float), tolerance(float), and a feedback list
                correct_answer = obj.get("correctAnswer")
                feedbacks = obj.get("feedbacks")
                tolerance = obj.get("tolerance")
                if not isinstance(correct_answer, float) or not isinstance(tolerance, float):
                    return False
                if not feedbacks:
                    return False

            case "drawing":
                # Drawing questions must have the same checks as word
                # but also a default answer and widget key
                correct_answer = obj.get("correctAnswer")
                default_answer = obj.get("defaultAnswer")
                correct_feedback = obj.get("correctFeedback")
                incorrect_feedback = obj.get("incorrectFeedback")
                widget_key = obj.get("widgetKey")
                if not correct_answer or not correct_feedback or not incorrect_feedback:
                    return False
                if (
                    not isinstance(correct_answer, str)
                    or not isinstance(default_answer, str)
                    or not isinstance(widget_key, str)
                ):
                    return False

            case n:
                raise TypeError(f"Attempted to verify unknown or illegal question type: {n}")

        return True

    @staticmethod
    def _normalisefigures(image_path: str | list[str] | None) -> list[str] | None:
        """Converts supported figures JSON formats to the internal representation.

        Accepted empty formats are `""`, `[""]`, and `[]`. All of these map to `None`.
        Non-empty strings are wrapped in a single-item list for consistency.
        """
        if image_path is None:
            return None

        if isinstance(image_path, str):
            cleaned = image_path.strip()
            return [cleaned] if cleaned else None

        if isinstance(image_path, list):
            cleaned = [
                path.strip() for path in image_path if isinstance(path, str) and path.strip()
            ]
            return cleaned or None

        return None
