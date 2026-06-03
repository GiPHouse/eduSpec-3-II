import json

from managers.QuestionManager import QuestionManager
from Quiz import Quiz
from validators.quizValidation import validateQuizObject


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
            ValueError: When encountering a malformed quiz or question.

        Returns:
            Quiz: The built quiz, with all built questions inside.
        """
        obj = json.loads(data)

        problems = validateQuizObject(obj)

        if len(problems) > 0:
            raise ValueError(f"Malformed quiz! The following problems were found: {problems}")

        name = obj.get("id")
        question_names = obj.get("questionNames")

        questions = []

        for question_name in question_names:
            try:
                question = QuestionManager.loadQuestion(question_name)
                questions.append(question)
            except Exception as e:
                raise e

        return Quiz(name, questions)
