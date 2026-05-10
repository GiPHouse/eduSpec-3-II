import json

from questions.IntegerQuestion import IntegerQuestion
from questions.MoleculeDrawingQuestion import MoleculeDrawingQuestion
from questions.MultipleChoiceQuestion import MultipleChoiceQuestion
from questions.Question import Question
from questions.SpectralQuestion import SpectralQuestion
from questions.WordQuestion import WordQuestion


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
            case IntegerQuestion():
                return cls._convertIntegerQuestion(question)
            case MoleculeDrawingQuestion():
                return cls._convertDrawingQuestion(question)
            case WordQuestion():
                return cls._convertWordQuestion(question)
            case SpectralQuestion():
                return cls._convertSpectralQuestion(question)
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
            - figures (dict): The image path. Empty if None
            - answers (array): The possible answers
            - correctAnswer (number): The correct answer as index of answers
            - feedbacks (array): The feedbacks given at each answer
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
    def _convertIntegerQuestion(cls, question: IntegerQuestion) -> str:
        """Serialises an IntegerQuestion to JSON

        Args:
            question (IntegerQuestion): The integer question to convert

        Returns:
            str: The generated JSON

           The JSON has the following template:
            - id (string): The question id
            - version (number): The saved version
            - type (string) "multipleChoice": The question type
            - title (string): The question title
            - bodyText (string): The question body text
            - figures (dict): The image path. Empty if None
            - lowerBound (int): The lowest correct answer
            - upperBound (int): The highest correct answer
            - feedbacks (array): The feedbacks given at each stage (correct, too low, too high)
        """
        data_out = cls._buildGenericQuestion(question)

        # ! Version number is hardcoded and updated when editing this function or _buildGenericQuestion
        data_out["version"] = 1
        data_out["type"] = "integer"

        data_out["lowerBound"] = question.correct_answer[0]
        data_out["upperBound"] = question.correct_answer[1]

        data_out["feedbacks"] = question.feedbacks

        return json.dumps(data_out)

    @classmethod
    def _convertWordQuestion(cls, question: WordQuestion) -> str:
        """Serialises a WordQuestion to JSON

        Args:
            question (WordQuestion): The word question to convert

        Returns:
            str: The generated JSON

            The JSON has the following template:
            - id (string): The question id
            - version (number): The saved version
            - type (string) "multipleChoice": The question type
            - title (string): The question title
            - bodyText (string): The question body text
            - figures (dict): The image path. Empty if None
            - correctAnswer (string): The correct answer to the question
            - correctFeedback (string): The feedback given if the answer was correct
            - incorrectFeedback (string): The feedback given if the answer was incorrect
        """
        data_out = cls._buildGenericQuestion(question)

        # ! Version number is hardcoded and updated when editing this function or _buildGenericQuestion
        data_out["version"] = 1
        data_out["type"] = "word"

        data_out["correctAnswer"] = question.correct_answer

        data_out["correctFeedback"] = question.feedbacks[0]
        data_out["incorrectFeedback"] = question.feedbacks[1]

        return json.dumps(data_out)

    @classmethod
    def _convertSpectralQuestion(cls, question: SpectralQuestion) -> str:
        """Serialises an SpectralQuestion to JSON

        Args:
            question (SpectralQuestion): The spectral question to convert

        Returns:
            str: The generated JSON

           The JSON has the following template:
            - id (string): The question id
            - version (number): The saved version
            - type (string) "multipleChoice": The question type
            - title (string): The question title
            - bodyText (string): The question body text
            - figures (list[dict]): The image path. Empty if None
            - spectralpath (string): the image path for spectral. Cannot be empty
            - correctAnswer (float): The correct answer.
            - feedbacks (array): The feedbacks given at each stage (correct, wrong or anything that the client specifies)
            - tolerance (float): How off can the user input be from the correct answer.
        """
        data_out = cls._buildGenericQuestion(question)

        # ! Version number is hardcoded and updated when editing this function or _buildGenericQuestion
        data_out["version"] = 1
        data_out["type"] = "spectral"

        data_out["spectralpath"] = question.spectralpath

        data_out["correctAnswer"] = question.correct_answer

        data_out["feedbacks"] = question.feedbacks
        data_out["tolerance"] = question.tolerance

        return json.dumps(data_out)

    @classmethod
    def _convertDrawingQuestion(cls, question: MoleculeDrawingQuestion) -> str:
        """Serialises a MoleculeDrawingQuestion to JSON

        Args:
            question (MoleculeDrawingQuestion): The drawing question to convert

        Returns:
            str: The generated JSON

           The JSON has the following template:
            - id (string): The question id
            - version (number): The saved version
            - type (string) "multipleChoice": The question type
            - title (string): The question title
            - bodyText (string): The question body text
            - figures (dict): The image path. Empty if None
            - correctAnswer (string): The correct answer
            - defaultAnswer (string): The initial answer given
            - correctFeedback (string): The feedback given if the answer was correct
            - incorrectFeedback (string): The feedback given if the answer was incorrect
            - widgetKey (string): The widget key used for the JSME component
        """
        data_out = cls._buildGenericQuestion(question)

        # ! Version number is hardcoded and updated when editing this function or _buildGenericQuestion
        data_out["version"] = 1
        data_out["type"] = "drawing"

        data_out["correctAnswer"] = question.correct_answer
        data_out["defaultAnswer"] = question.default

        data_out["correctFeedback"] = question.feedbacks[0]
        data_out["incorrectFeedback"] = question.feedbacks[1]

        data_out["widgetKey"] = question.widget_key

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
            - figures (dict): The image path. Empty if None
        """
        # ! Versioning is done in the individual functions. When updating this function, increase all by 100
        data_out = {}

        data_out["id"] = question.name
        data_out["title"] = question.title
        data_out["bodyText"] = question.bodytext
        data_out["bodyFormat"] = getattr(question, "body_format", "text")

        figures = question.figures
        if figures is None:
            data_out["figures"] = []
        else:
            data_out["figures"] = figures

        return data_out
