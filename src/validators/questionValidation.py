"""Validator module for questions.

Stuff to check (generic):
    - id is a nonnull string
    - if there is a file name, it must match the id
    - title is a nonnull string
    - bodyText is a string
    - version is a positive integer
    - figures (optional) is either:
        - a list of strings
        - a list of dicts, which contain
            - path: string
            - description: string
    - bodyFormat (optional) is either
        - "text"
        - "latex"
    - type is either of the following:
        - ["integer", "multipleChoice", "spectral", "word", "drawing"]

Stuff to check (integer):
    - checker (optional) is a nonnull string
    OR all of the below:
    - lowerBound is an int or float
    - upperBound is an int or float
    - upperBound is greater or equal to lowerBound
    - feedbacks is a list of 3 nonnull strings

Stuff to check (multipleChoice):
    - answers is a list of 2 or more nonnull strings
    - checker (optional) is a nonnull string
    OR all of the below:
    - feedbacks is a list of nonnull strings of the same length as answers
    - correctAnswer is an integer >=0 and <len(answers)

Stuff to check (spectral):
    - spectralpath is a nonnull string
    - checker (optional) is a nonnull string
    OR all of the below:
    - feedbacks is a 2-element list of nonnull strings
    - correctAnswer is an int or float
    - tolerance (optional) is an int or float

Stuff to check (word):
    - checker (optional) is a nonnull string
    OR all of the below:
    - correctFeedback is a nonnull string
    - incorrectFeedback is a nonnull string
    - correctAnswer is a nonnull string

Stuff to check (drawing):
    - defaultAnswer (optional) is a string
    - widgetKey (optional) is a string
    All of the checks for word
"""

import json
from pathlib import Path


def validateQuestionFile(file_to_check: str | Path) -> list[str]:
    """Checks a file to see if it's valid.

    This has more checks than `validateQuestion()`.

    Args:
        file_to_check (str|Path): The file to check.

    Returns:
        list[str]: A list of problems. If it's empty the question is valid.
    """
    if not isinstance(file_to_check, Path):
        file_to_check = Path(file_to_check)
    file_to_check = file_to_check.resolve()
    with open(file_to_check) as f:
        contents = f.read()
        obj = json.loads(contents)
        return validateQuestionObject(obj, file_name=file_to_check)


def validateQuestion(to_check: str) -> list[str]:
    """Checks a json question to see if it's valid.

    Args:
        to_check (str): The json to check.

    Returns:
        list[str]: A list of problems. If it's empty the question is valid.
    """
    return validateQuestionObject(json.loads(to_check))


def validateQuestionObject(obj: dict, **kwargs) -> list[str]:
    """Checks a json-loaded question object to see if it's valid.

    Args:
        object (dict): The json object to check.

    Kwargs:
        file_name (str), optional: The filename of the quiz.

    Returns:
        list[str]: A list of problems. If it's empty the question is valid.
    """
    problems = []

    file_name = kwargs.get("file_name", None)

    attr_id = obj.get("id", None)
    if attr_id is None:
        # Check whether id exists
        problems.append("Questions must have an `id` attribute. This should be a non-empty string.")

    elif not isinstance(attr_id, str) or attr_id == "":
        # Check whether id is a non-empty string
        problems.append("The `id` attribute must be a non-empty string.")

    elif file_name is not None:
        # Double-check whether the filename is a path
        if not isinstance(file_name, Path):
            problems.append("File name was specified, but was not a pathlib.Path.")

        # Check whether the filename matches the id.
        else:
            file_name_final = file_name.name
            if not file_name_final.split(".")[0] == attr_id:
                problems.append(
                    f"File name and `id` should be the same. Found file name '{file_name_final.split('.')[0]}' and id '{attr_id}'."
                )

    attr_title = obj.get("title", None)
    if attr_title is None:
        # Check whether title exists
        problems.append(
            "Questions must have an `title` attribute. This should be a non-empty string."
        )

    elif not isinstance(attr_title, str) or attr_title == "":
        # Check whether title is a non-empty string
        problems.append("The `title` attribute must be a non-empty string.")

    attr_bodytext = obj.get("title", None)
    if attr_bodytext is None:
        # Check whether bodyText exists
        problems.append(
            "Questions must have an `bodyText` attribute. This should be a non-empty string."
        )

    elif not isinstance(attr_bodytext, str):
        # Check whether bodyText is a non-empty string
        problems.append("The `bodyText` attribute must be a string.")

    attr_version = obj.get("version")
    if attr_version is None:
        # Check whether version exists
        problems.append(
            "Questions must have a `version` attribute. This should be a positive integer."
        )

    elif not isinstance(attr_version, int) or attr_version < 1:
        # Check whether version is a positive integer
        problems.append("The `version` attribute must be a positive integer.")

    attr_type = obj.get("type")
    if attr_type is None:
        # Check whether type exists
        problems.append(
            'Questions must have a `type` attribute. This must be one of the following: "drawing", "integer", "multipleChoice", "spectral", or "word".'
        )

    elif not isinstance(attr_type, str) or attr_type not in [
        "integer",
        "multipleChoice",
        "spectral",
        "word",
        "drawing",
    ]:
        # Check whether type is a valid type
        problems.append(
            'The `type` attribute must be one of the following: "drawing", "integer", "multipleChoice", "spectral", or "word".'
        )

    attr_bodyformat = obj.get("bodyFormat", None)
    if attr_bodyformat is not None and (
        not isinstance(attr_bodyformat, str) or attr_bodytext not in ["text", "latex"]
    ):
        # Check whether bodyText is "text" or "latex"
        problems.append(
            'The `bodyFormat` attribute must be either "text" or "latex". If you do not want to specify it, leave it out and it will default to text.'
        )

    attr_figures = obj.get("figures", None)
    if attr_figures is None:
        # Figures is not required
        pass

    elif not isinstance(attr_figures, list):
        # Check whether questionNames is a list
        problems.append(
            "The `figures` attribute must be a list. If you do not wish to have figures leave it out."
        )

    else:
        if any([not isinstance(x, (str, dict)) for x in attr_figures]):
            # Check whether figures only contains strings and dicts
            problems.append(
                "The `figures` attribute must only contain strings or dictionaries. You currently have a non-string, non-dict entry in it."
            )

        if any([isinstance(x, str) and x == "" for x in attr_figures]):
            # Check whether figures only contains non-empty strings (and dicts)
            problems.append(
                "The `figures` attribute must only contain non-empty strings or dictionaries. You currently have an empty string in it."
            )

        if any(
            [
                isinstance(x, dict)
                and (
                    x.get("path", None) is None
                    or not isinstance(x.get("path", None), str)
                    or x.get("path", None) == ""
                    or x.get("description", None) is None
                    or not isinstance(x.get("description", None), str)
                    or x.get("description", None) == ""
                )
                for x in attr_figures
            ]
        ):
            # Check whether figures only contains correctly-shaped dicts (and strings)
            problems.append(
                "The `figures` attribute must only contain strings or dictionaries with non-empty strings under the `path` and `description` keys. You currently have a broken dictionary in it."
            )

    if attr_type in ["integer", "multipleChoice", "spectral", "word", "drawing"]:
        match attr_type:
            case "integer":
                problems.extend(_validateIntegerQuestion(obj))

            case "multipleChoice":
                problems.extend(_validateMultipleChoiceQuestion(obj))

            case "spectral":
                problems.extend(_validateSpectralQuestion(obj))

            case "word":
                problems.extend(_validateWordQuestion(obj))

            case "drawing":
                problems.extend(_validateDrawingQuestion(obj))

    return problems


def _validateIntegerQuestion(obj: dict) -> list[str]:
    """Checks a json-loaded integer question object to see if it's valid.

    This only checks the integer question-specific attributes, not generic.

    Args:
        obj (dict): The json object to check.

    Returns:
        list[str]: A list of problems. If it's empty the integer-specific parts of the question are valid.
    """
    problems = []

    attr_checker = obj.get("checker", None)
    if attr_checker is not None:
        # If checker does not exist, standard checking is used
        if not isinstance(attr_checker, str) or attr_checker == "":
            # Check whether checker is a nonnull string, if it exists
            problems.append(
                "The `checker` attribute should be a non-empty string. If you do not want to use a custom checker, leave it out."
            )

        return problems

    attr_lowerbound = obj.get("lowerBound", None)
    if attr_lowerbound is None:
        # Check whether lowerBound exists
        problems.append(
            "Integer questions must have a `lowerBound` attribute. This should be an int or float."
        )

    elif not isinstance(attr_lowerbound, (int, float)):
        # Check whether lowerBound is an int
        problems.append("The `lowerBound` attribute should be an int or float.")

    attr_upperbound = obj.get("upperBound", None)
    if attr_upperbound is None:
        # Check whether upperbound exists
        problems.append(
            "Integer questions must have a `upperBound` attribute. This should be an int or float."
        )

    elif not isinstance(attr_upperbound, (int, float)):
        # Check whether upperbound is an int
        problems.append("The `upperBound` attribute should be an int or float.")

    if (
        isinstance(attr_lowerbound, (int, float))
        and isinstance(attr_upperbound, (int, float))
        and attr_upperbound < attr_lowerbound
    ):
        # Check whether lowerbound is lower than upperbound
        problems.append(
            "The upper bound of an integer question must be higher than or equal to the lower bound"
        )

    attr_feedbacks = obj.get("feedbacks", None)
    if attr_feedbacks is None:
        # Check whether feedbacks exists
        problems.append(
            "Integer questions must have a `feedbacks` attribute. This should be a list of 3 non-empty strings"
        )

    elif not isinstance(attr_feedbacks, list):
        # Check whether feedbacks is a list
        problems.append("The `feedbacks` attribute must be a list.")

    elif len(attr_feedbacks) != 3:
        # Check whether feedbacks is 3 long
        problems.append("The `feedbacks` attribute must have a length of 3")

    elif any([not isinstance(x, str) or x == "" for x in attr_feedbacks]):
        # Check whether feedbacks only contains non-empty strings
        problems.append(
            "The `feedbacks` attribute must only contain non-empty strings. You currently have an empty string or non-string in it."
        )

    return problems


def _validateMultipleChoiceQuestion(obj: dict) -> list[str]:
    """Checks a json-loaded multiple-choice question object to see if it's valid.

    This only checks the multiple-choice question-specific attributes, not generic.

    Args:
        obj (dict): The json object to check.

    Returns:
        list[str]: A list of problems. If it's empty the multiple-choice-specific parts of the question are valid.
    """
    problems = []

    attr_answers = obj.get("answers", None)
    if attr_answers is None:
        # Check if answers exists
        problems.append(
            "Multiple-choice questions must have an `answers` attribute. This should be a list of non-empty strings."
        )

    elif not isinstance(attr_answers, list):
        # Check whether answers is a list
        problems.append("The `answers` attribute should be a list.")

    else:
        if any(not isinstance(x, str) or x == "" for x in attr_answers):
            # Check whether answers is filled with nonnull strings
            problems.append(
                "The `answers` attribute should only contain non-empty strings. You currently have an empty string or non-string in it."
            )

        if len(attr_answers) < 2:
            # Check that there are at least 2 answers
            problems.append(
                "The `answers` attribute should contain at least two elements. You have less than that."
            )

    attr_checker = obj.get("checker", None)
    if attr_checker is not None:
        # If checker does not exist, standard checking is used
        if not isinstance(attr_checker, str) or attr_checker == "":
            # Check whether checker is a nonnull string, if it exists
            problems.append(
                "The `checker` attribute should be a non-empty string. If you do not want to use a custom checker, leave it out."
            )

        return problems

    attr_feedbacks = obj.get("feedbacks", None)
    if attr_feedbacks is None:
        # Check if feedbacks exists
        problems.append(
            "Multiple-choice questions must have a `feedbacks` attribute. This should be a list of non-empty strings."
        )

    elif not isinstance(attr_feedbacks, list):
        # Check whether feedbacks is a list
        problems.append("The `answers` attribute should be a list.")

    else:
        if any(not isinstance(x, str) or x == "" for x in attr_feedbacks):
            # Check whether feedbacks is filled with nonnull strings
            problems.append(
                "The `feedback` attribute should only contain non-empty strings. You currently have an empty string or non-string in it."
            )

        if isinstance(attr_answers, list) and len(attr_feedbacks) != len(attr_answers):
            # Check that there is feedback for every answer
            problems.append(
                f"The `feedback` attribute should have the same length as the `answers` attribute. Currently there are {len(attr_feedbacks)} feedbacks for {len(attr_answers)} answers."
            )

    attr_correctanswer = obj.get("correctAnswer", None)
    if attr_correctanswer is None:
        # Check whether correct answer exists
        problems.append(
            "Multiple-choicelist of non-empty strings questions must have a `correctAnswer` attribute. This should be an integer between 0 and the amount of answers."
        )

    elif not isinstance(attr_correctanswer, int):
        # Check whether correct answer is an int.
        problems.append("The `correctAnswer` attribute should be an integer.")

    elif attr_correctanswer < 0 or (
        isinstance(attr_answers, list) and attr_correctanswer >= len(attr_answers)
    ):
        # Check whether correct answer is a valid answer
        problems.append(
            "The `correctAnswer` attribute should be no lower than zero and not equal or higher than the amount of answers."
        )

    return problems


def _validateSpectralQuestion(obj: dict) -> list[str]:
    """Checks a json-loaded spectral question object to see if it's valid.

    This only checks the spectral question-specific attributes, not generic.

    Args:
        obj (dict): The json object to check.

    Returns:
        list[str]: A list of problems. If it's empty the spectral-specific parts of the question are valid.
    """
    problems = []

    attr_path = obj.get("spectralpath", None)
    if attr_path is None:
        # Check whether spectral path exists
        problems.append(
            "Spectral questions must have a `spectralpath` attribute. This should be a non-empty string."
        )

    elif not isinstance(attr_path, str) or attr_path == "":
        # Check whether spectral path is a nonnull string
        problems.append("The `spectralpath` attribute should be a non-empty string.")

    attr_checker = obj.get("checker", None)
    if attr_checker is not None:
        # If checker does not exist, standard checking is used
        if not isinstance(attr_checker, str) or attr_checker == "":
            # Check whether checker is a nonnull string, if it exists
            problems.append(
                "The `checker` attribute should be a non-empty string. If you do not want to use a custom checker, leave it out."
            )

        return problems

    attr_feedbacks = obj.get("feedbacks")
    if attr_feedbacks is None:
        # Check whether feedbacks exists
        problems.append(
            "Spectral questions must have a `feedbacks` attribute. This should be a list of 2 non-empty strings"
        )

    elif not isinstance(attr_feedbacks, list):
        # Check whether feedbacks is a list
        problems.append("The `feedbacks` attribute must be a list.")

    elif len(attr_feedbacks) != 3:
        # Check whether feedbacks is 3 long
        problems.append(
            "The `feedbacks` attribute must have a length of 3. It is sorted as 'correct feedback', 'too low feedback', 'too high feedback'."
        )

    attr_correctanswer = obj.get("correctAnswer", None)
    if attr_correctanswer is None:
        # Check whether correct answer exists
        problems.append(
            "Spectral questions must have a `correctAnswer` attribute. This should be an int or float."
        )

    elif not isinstance(attr_correctanswer, (int, float)):
        # Check whether correct answer is an int or float
        problems.append(
            f"The `correctAnswer` attribute should be an int or float. Currently it is {type(attr_correctanswer)}"
        )

    attr_tolerance = obj.get("tolerance", None)
    if attr_tolerance is not None and not isinstance(attr_tolerance, (int, float)):
        # Check whether tolerance is an int or float
        problems.append(
            f"The `tolerance` attribute should be an int or float. Currently it is {type(attr_tolerance)}. You can leave it out, and it will default to 0.5."
        )

    return problems


def _validateWordQuestion(obj: dict) -> list[str]:
    """Checks a json-loaded word question object to see if it's valid.

    This only checks the word question-specific attributes, not generic.

    Args:
        obj (dict): The json object to check.

    Returns:
        list[str]: A list of problems. If it's empty the word-specific parts of the question are valid.
    """
    problems = []

    attr_checker = obj.get("checker", None)
    if attr_checker is not None:
        # If checker does not exist, standard checking is used
        if not isinstance(attr_checker, str) or attr_checker == "":
            # Check whether checker is a nonnull string, if it exists
            problems.append(
                "The `checker` attribute should be a non-empty string. If you do not want to use a custom checker, leave it out."
            )

        return problems

    attr_correctanswer = obj.get("correctAnswer", None)
    if attr_correctanswer is None:
        # Check whether correct answer exists
        problems.append(
            "Word questions must have a `correctAnswer` attribute. This should be a non-empty string."
        )

    elif not isinstance(attr_correctanswer, str) or attr_correctanswer == "":
        # Check whether correct answer is a nonnull string
        problems.append("The `correctAnswer` attribute should be a non-empty string.")

    attr_correctfeedback = obj.get("correctFeedback", None)
    if attr_correctfeedback is None:
        # Check whether correct feedback exists
        problems.append(
            "Word questions must have a `correctFeedback` attribute. This should be a non-empty string."
        )

    elif not isinstance(attr_correctfeedback, str) or attr_correctfeedback == "":
        # Check whether correct feedback is a nonnull string
        problems.append("The `correctFeedback` attribute should be a non-empty string.")

    attr_incorrectfeedback = obj.get("incorrectFeedback", None)
    if attr_incorrectfeedback is None:
        # Check whether incorrect feedback exists
        problems.append(
            "Word questions must have a `incorrectFeedback` attribute. This should be a non-empty string."
        )

    elif not isinstance(attr_incorrectfeedback, str) or attr_incorrectfeedback == "":
        # Check whether incorrect feedback is a nonnull string
        problems.append("The `incorrectFeedback` attribute should be a non-empty string.")

    return problems


def _validateDrawingQuestion(obj: dict) -> list[str]:
    """Checks a json-loaded drawing question object to see if it's valid.

    This only checks the drawing question-specific attributes, not generic.

    Args:
        obj (dict): The json object to check.

    Returns:
        list[str]: A list of problems. If it's empty the drawing-specific parts of the question are valid.
    """
    problems = []

    attr_defaultanswer = obj.get("defaultAnswer", None)
    if attr_defaultanswer is not None:
        # Default answer is not required
        if not isinstance(attr_defaultanswer, str) or attr_defaultanswer == "":
            # Check whether default answer is a nonnull string, if it exists
            problems.append(
                "The `defaultAnswer` attribute should be a non-empty string. If you do not want to use it, leave it out."
            )

    attr_widgetkey = obj.get("widgetKey", None)
    if attr_widgetkey is not None:
        # Default answer is not required
        if not isinstance(attr_widgetkey, str) or attr_widgetkey == "":
            # Check whether default answer is a nonnull string, if it exists
            problems.append(
                "The `widgetKey` attribute should be a non-empty string. If you do not want to use it, leave it out."
            )

    word_problems = _validateWordQuestion(obj)
    word_problems = [x.replace("Word", "Drawing") for x in word_problems]

    problems.extend(word_problems)

    return problems
