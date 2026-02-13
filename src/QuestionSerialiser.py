from Question import Question
from MultipleChoiceQuestion import MultipleChoiceQuestion

class QuestionSerialiser():
    """Class to convert any question to JSON
    """
    
    @classmethod
    def questionToJson(cls, question: Question) -> str:
        """Converts any question to JSON. Do not use the parent Question class.

        Args:
            question (Question): The question to convert

        Raises:
            ValueError: Raises a ValueError on an unrecognised question type

        Returns:
            str: The generated JSON
        """
        match question:
            case MultipleChoiceQuestion():
                return cls._convertMultipleChoiceQuestion(question)
            case n:
                raise ValueError(f"Unknown or illegal question type encountered: {n.__class__}")
            
    @staticmethod
    def _convertMultipleChoiceQuestion(question: MultipleChoiceQuestion) -> str:
        """Serialises a MultipleChoiceQuestion to JSON

        Args:
            question (MultipleChoiceQuestion): The multiple-choice question to convert

        Returns:
            str: The generated JSON
        """
        return ""