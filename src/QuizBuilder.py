import json

from QuestionManager import QuestionManager
from Quiz import Quiz


class QuizBuilder:
    """Builder class for quizzes.

    This will take in json and build quizzes instantiated with questions
    """

    @staticmethod
    def quizFromJson(data: str) -> Quiz:
        """Builds a quiz from json data.

        Will only work with correct data, otherwise it'll raise errors.
        This will also load and build all questions within the quiz.

        Args:
            data (str): The json string describing the quiz.

        Raises:
            TypeError: When encountering an unrecognised question type.
            ValueError: When encountering a malformed question or quiz.

        Returns:
            Quiz: The built quiz, with all built questions inside.
        """
        obj = json.loads(data)

        name = obj.get("id")
        question_names = obj.get("questionNames")

        if not name:
            raise ValueError("Malformed quiz! Missing id.")

        if not question_names:
            raise ValueError(f"Malformed quiz {id}! Missing questions.")

        questions = []

        for question_name in question_names:
            try:
                question = QuestionManager.loadQuestion(question_name)
                questions.append(question)
            except FileNotFoundError:
                raise ValueError(f"Malformed quiz {id}! Question {question_name} does not exist.")
            except Exception as e:
                raise e

        return Quiz(name, questions)
