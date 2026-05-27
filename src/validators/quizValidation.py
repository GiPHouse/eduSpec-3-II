"""Validator module for quizzes

Stuff to check:

- id is a nonnull string
    * fix: adds an id based on the filename if present
    ! fix: overrides id if it's not a string
- if there is a file name, it must match the id
    ! fix: renames the file
- questionNames is a list of nonnull strings
    * fix: turn a single string into a list
    * fix: purge any empty strings
    ! fix: purge any non-string entries
- all questions included exist
- no further attributes should exist
"""

import json
from pathlib import Path
from typing import cast

from managers.QuestionManager import QuestionManager


def validateQuizFile(file_to_check: str | Path) -> list[str]:
    """Checks a file to see if it's valid.

    This has more checks than `validateQuiz()`.

    Args:
        file_to_check (str|Path): The file to check.

    Returns:
        list[str]: A list of problems. If it's empty the quiz is valid.
    """
    if not isinstance(file_to_check, Path):
        file_to_check = Path(file_to_check)
    file_to_check = file_to_check.resolve()
    with open(file_to_check) as f:
        contents = f.read()
        obj = json.loads(contents)
        return validateQuizObject(obj, file_name=file_to_check)


def validateQuiz(to_check: str) -> list[str]:
    """Checks a json quiz to see if it's valid.

    Args:
        to_check (str): The json to check.

    Returns:
        list[str]: A list of problems. If it's empty the quiz is valid.
    """
    return validateQuizObject(json.loads(to_check))


def validateQuizObject(obj: dict, **kwargs) -> list[str]:
    """Checks a json-loaded quiz object to see if it's valid.

    Args:
        object (dict): The json object to check.

    Kwargs:
        file_name (str), optional: The filename of the quiz.

    Returns:
        list[str]: A list of problems. If it's empty the quiz is valid.
    """
    problems = []

    file_name = kwargs.get("file_name", None)

    attr_id = obj.get("id", None)
    if attr_id is None:
        # Check whether id exists
        problems.append("Quizzes must have an `id` attribute. This should be a non-empty string.")

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

    attr_questions = obj.get("questionNames", None)
    if attr_questions is None:
        # Check whether questionNames exists
        problems.append(
            "Quizzes must have a `questionNames` attribute. This should be a list of strings of question ids."
        )

    elif not isinstance(attr_questions, list):
        # Check whether questionNames is a list
        problems.append("The `questionNames` attribute must be a list.")

    elif any([not isinstance(x, str) or x == "" for x in attr_questions]):
        # Check whether questionNames only contains non-empty strings
        problems.append(
            "The `questionNames` attribute must only contain question ids. You currently have an empty string or non-string in it."
        )

    else:
        # Check whether all questions exist
        for question_name in attr_questions:
            if not QuestionManager.itemExists(question_name):
                problems.append(
                    f"The question '{question_name}' included in `questionNames` does not exist."
                )

    # Check for excess attributes
    # (Booleans can be summed and are 1)
    found_attributes = ("id" in obj.keys()) + ("id" in obj.keys())
    if len(obj.keys()) > found_attributes:
        if found_attributes == 2:
            problems.append(
                "You have too many attributes. Only `id` and `questionNames` will be used"
            )

        else:
            problems.append("You have misspelled an attribute or have too many attributes.")

    return problems


def fixQuizFile(file_to_check: str | Path, unsafe_fixes: bool = False) -> list[str]:
    """Validates and fixes a quiz file.

    This does not guarantee the quiz to be fixed afterwards, as not every error can be fixed.

    Args:
        file (str|Path): The file to check.
        unsafe_fixes (bool): Whether to do apply less safe fixes. This will fix more things but can cause damage.

    Returns:
        list[str]: A list of fixes applied.
    """
    if not isinstance(file_to_check, Path):
        file_to_check = Path(file_to_check)
    file_to_check = file_to_check.resolve()
    with open(file_to_check) as f:
        contents = f.read()
        obj = json.loads(contents)
        cast(dict, obj)

    fixes = []

    # Create an id if missing
    attr_id = obj.get("id", None)
    if attr_id is None or attr_id == "":
        obj["id"] = file_to_check.name.split(".")[0]
        fixes.append("Added missing `id` attribute.")

    # Overwrite the id if it's not a string
    elif not isinstance(attr_id, str) and unsafe_fixes:
        obj["id"] = file_to_check.name.split(".")[0]
        fixes.append("!Turned `id` into string!")

    # Rename file if it doesn't match id
    elif file_to_check.name.split(".")[0] != attr_id:
        parent_folder = file_to_check.parent
        new_file = parent_folder.joinpath(f"{attr_id}.py")
        file_to_check = file_to_check.rename(new_file)
        fixes.append(f"!Renamed file to {attr_id}")

    # Turn a string into a singleton list
    attr_questions = obj.get("questionNames", None)
    if isinstance(attr_questions, str):
        obj["questionNames"] = [attr_questions]

    # Remove empty strings
    # Remove non-strings
    if isinstance(attr_questions, list):
        for question in attr_questions:
            if question == "":
                attr_questions.remove(question)
                fixes.append("Removed empty value from `questionNames.`")

            if not isinstance(question, str) and unsafe_fixes:
                attr_questions.remove(question)
                fixes.append(f"!Removed non-string value {question} from `questionNames`!")

    with open(file_to_check, "w") as f:
        new_json = json.dumps(obj)
        f.write(new_json)
    return fixes
