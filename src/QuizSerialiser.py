import json

from Quiz import Quiz


class QuizSerialiser:
    """Class to convert quizzes to json."""

    @staticmethod
    def quizToJson(quiz: Quiz) -> str:
        """Serialises a quiz to json.

        This does not save the questions. Do that separately

        Args:
            quiz (Quiz): The quiz to serialise to json.

        Returns:
            str: The serialised json.
        """
        data_out = {}

        data_out["id"] = quiz.name

        question_names = [question.name for question in quiz.question_list]

        data_out["questionNames"] = question_names

        return json.dumps(data_out)
