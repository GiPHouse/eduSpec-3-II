"""Validator module for questions.

Stuff to check (generic):
    - id is a nonnull string
    - title is a nonnull string
    - bodyText is a string
    - version is a positive integer
    - figures is either:
        - a list of strings
        - a list of dicts, which contain
            - path: string
            - description: string
    - bodyFormat is either
        - "text"
        - "latex"
    - type is either of the following:
        - ["integer", "multipleChoice", "spectral", "word", "drawing"]

Stuff to check (integer):
    - checker is a nonnull string
    OR all of the below:
    - lowerBound is an integer
    - upperBound is an integer
    - feedbacks is a list of 3 nonnull strings

Stuff to check (multipleChoice):
    - answers is a list of 2 or more nonnull strings
    - checker is a nonnull string
    OR all of the below:
    - feedbacks is a list of nonnull strings of the same length as answers
    - correctAnswer is an integer >=0 and <len(answers)

Stuff to check (spectral):
    - spectralpath is a nonnull string
    - checker is a nonnull string
    OR all of the below:
    - feedbacks is a 2-element list of nonnull strings
    - correctAnswer is an int or float
    - tolerance is an int or float

Stuff to check (word):
    - checker is a nonnull string
    OR all of the below:
    - correctFeedback is a nonnull string
    - incorrectFeedback is a nonnull string
    - correctAnswer is a nonnull string

Stuff to check (drawing):
    - defaultAnswer is a string
    - widgetKey is a string
    All of the checks for word


"""

import json
from pathlib import Path


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

    elif not isinstance(attr_bodytext, str) or attr_bodytext == "":
        # Check whether bodyText is a non-empty string
        problems.append("The `bodyText` attribute must be a non-empty string.")

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
    if attr_bodyformat is None:
        # Check whether bodyText exists
        problems.append(
            'Questions must have an `bodyFormat` attribute. This should be either "text" or "latex".'
        )

    elif not isinstance(attr_bodyformat, str) or attr_bodytext not in ["text", "latex"]:
        # Check whether bodyText is "text" or "latex"
        problems.append('The `bodyText` attribute must be either "text" or "latex".')

    attr_figures = obj.get("figures", None)
    if attr_figures is None:
        # Check whether figures exists
        problems.append("Questions must have an `figures` attribute. This should be a list.")

    elif not isinstance(attr_figures, list):
        # Check whether questionNames is a list
        problems.append("The `figures` attribute must be a list.")

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

    return problems


def _validateIntegerQuestion(obj: dict) -> list[str]:
    """Checks a json-loaded integer question object to see if it valid.

    This only checks the integer question-specific attributes, not generic.

    Args:
        obj (dict): The json object to check.

    Returns:
        list[str]: A list of problems. If it's empty the integer-specific parts of the question are valid.
    """
    problems = []

    return problems
