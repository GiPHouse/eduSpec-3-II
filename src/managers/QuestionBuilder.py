import json

from managers.CheckerManager import CheckerManager
from managers.ScriptManager import ScriptManager
from questions.IntegerQuestion import IntegerQuestion
from questions.MoleculeDrawingQuestion import MoleculeDrawingConfig, MoleculeDrawingQuestion
from questions.MultipleChoiceQuestion import MultipleChoiceQuestion
from questions.Question import Question
from questions.ScriptQuestion import ScriptQuestion
from questions.SpectralQuestion import SpectralQuestion
from questions.WordQuestion import WordQuestion
from validators.questionValidation import validateQuestionObject


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
            ValueError: When encountering a malformed question.

        Returns:
            Question: The built question. This can be any question subtype, but will never be the interface/parent `Question` class.
        """
        obj = json.loads(data)

        problems = validateQuestionObject(obj)

        if len(problems) > 0:
            raise ValueError(f"Failed verifying {obj.get('id', 'question')}: {problems}")

        question_type = obj.get("type")
        obj.get("version")
        name = obj.get("id")
        title = obj.get("title")
        bodytext = obj.get("bodyText")
        body_format = obj.get("bodyFormat", "text")
        figures = obj.get("figures")
        spectralpath = obj.get("spectralpath")
        checker = obj.get("checker")
        checker_object = CheckerManager.buildChecker(checker) if checker else None
        download_data = obj.get("download_data")

        match question_type:
            case "multipleChoice":
                answers = obj.get("answers")
                feedbacks = None if checker_object else obj.get("feedbacks")
                correct_answer = None if checker_object else obj.get("correctAnswer")
                return MultipleChoiceQuestion(
                    name=name,
                    title=title,
                    bodytext=bodytext,
                    body_format=body_format,
                    answers=answers,
                    feedbacks=feedbacks,
                    correct_answer=correct_answer,
                    figures=figures,
                    download_data=download_data,
                    checker=checker_object,
                )

            case "integer":
                bounds = None if checker_object else (obj.get("lowerBound"), obj.get("upperBound"))
                feedbacks = None if checker_object else obj.get("feedbacks")
                return IntegerQuestion(
                    name=name,
                    title=title,
                    bodytext=bodytext,
                    body_format=body_format,
                    correct_answer=bounds,
                    feedbacks=feedbacks,
                    figures=figures,
                    download_data=download_data,
                    checker=checker_object,
                )

            case "word":
                correct_answer = None if checker_object else obj.get("correctAnswer")
                feedbacks = (
                    None
                    if checker_object
                    else [obj.get("correctFeedback"), obj.get("incorrectFeedback")]
                )
                return WordQuestion(
                    name=name,
                    title=title,
                    bodytext=bodytext,
                    body_format=body_format,
                    correct_answer=correct_answer,
                    feedbacks=feedbacks,
                    figures=figures,
                    download_data=download_data,
                    checker=checker_object,
                )

            case "spectral":
                correct_answer = None if checker_object else float(obj.get("correctAnswer"))
                feedbacks = None if checker_object else obj.get("feedbacks")
                tolerance = None if checker_object else float(obj.get("tolerance"))
                spectralpath = obj.get("spectralpath")

                return SpectralQuestion(
                    name=name,
                    title=title,
                    bodytext=bodytext,
                    body_format=body_format,
                    correct_answer=correct_answer,
                    feedbacks=feedbacks,
                    figures=figures,
                    spectralpath=spectralpath,
                    tolerance=tolerance,
                    download_data=download_data,
                    checker=checker_object,
                )

            case "drawing":
                feedbacks = (
                    None
                    if checker_object
                    else [obj.get("correctFeedback"), obj.get("incorrectFeedback")]
                )
                correct_answer = None if checker_object else obj.get("correctAnswer")
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
                    download_data=download_data,
                    checker=checker_object,
                )

            case "script":
                script_name = obj.get("script")
                parameters = obj.get("parameters", [])
                script = ScriptManager.buildScript(script_name)

                return ScriptQuestion(
                    name=name,
                    title=title,
                    bodytext=bodytext,
                    body_format=body_format,
                    script=script,
                    parameters=parameters,
                    figures=figures,
                    download_data=download_data,
                    checker=checker_object,
                )

            case n:
                raise TypeError(f"Attempted to build unknown or illegal question type: {n}")

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
