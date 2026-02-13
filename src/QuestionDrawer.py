from MultipleChoiceQuestion import MultipleChoiceQuestion
from Question import Question


class QuestionDrawer:
    """Connects the questions with streamlit"""

    @staticmethod
    def drawQuestion(current_question: Question) -> None:
        """Currently unimplemented. Will create a streamlit object for questions.

        Args:
            current_question (Question): The question to connect.
        """
        if current_question is MultipleChoiceQuestion:
            pass
