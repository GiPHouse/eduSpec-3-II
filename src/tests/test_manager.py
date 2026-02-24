import pathlib

from MultipleChoiceQuestion import MultipleChoiceQuestion
from QuestionManager import QuestionManager
from QuestionSerialiser import QuestionSerialiser


class TestManager:
    """Test cases for the question manager"""

    def test_SavingMCQ(self, tmp_path: pathlib.Path) -> None:
        """Test case for saving a multiple-choice question"""
        QuestionManager.save_location = tmp_path

        mcq = MultipleChoiceQuestion(
            "question1",
            "Example Question",
            "here's a question",
            ["a", "b", "c"],
            1,
            ["a: wrong", "b: correct", "c: wrong"],
        )

        assert QuestionManager.saveQuestion(mcq)

        expected_location = tmp_path.joinpath(f"{mcq.name}.json")

        assert expected_location.is_file()

        saved_data = expected_location.read_text()

        assert saved_data == QuestionSerialiser.questionToJson(mcq)

    def test_LoadMCQ(self, tmp_path: pathlib.Path) -> None:
        """Test case for loading a multiple-choice question"""
        QuestionManager.save_location = tmp_path

        location = tmp_path.joinpath("question1.json")
        location.touch()
        location.write_text(
            r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "imagePath": "", "version": 1, "type": "multipleChoice", "answers": ["a", "b", "c"], "correctAnswer": 1, "feedbacks": ["a: wrong", "b: correct", "c: wrong"]}"""
        )

        loaded_mcq = QuestionManager.loadQuestion("question1")

        mcq = MultipleChoiceQuestion(
            "question1",
            "Example Question",
            "here's a question",
            ["a", "b", "c"],
            1,
            ["a: wrong", "b: correct", "c: wrong"],
        )

        assert isinstance(loaded_mcq, MultipleChoiceQuestion)

        assert mcq.name == loaded_mcq.name
        assert mcq.title == loaded_mcq.title
        assert mcq.bodytext == loaded_mcq.bodytext
        assert mcq.imgpath == loaded_mcq.imgpath
        assert mcq.answers == loaded_mcq.answers
        assert mcq.feedbacks == loaded_mcq.feedbacks
        assert mcq.correct_answer == loaded_mcq.correct_answer

    def test_CycleMCQ(self, tmp_path: pathlib.Path) -> None:
        """Test case for saving then loading a multiple-choice question"""
        QuestionManager.save_location = tmp_path

        mcq = MultipleChoiceQuestion(
            "question1",
            "Example Question",
            "here's a question",
            ["a", "b", "c"],
            1,
            ["a: wrong", "b: correct", "c: wrong"],
        )

        assert QuestionManager.saveQuestion(mcq)

        loaded_mcq = QuestionManager.loadQuestion("question1")

        assert isinstance(loaded_mcq, MultipleChoiceQuestion)

        assert mcq.name == loaded_mcq.name
        assert mcq.title == loaded_mcq.title
        assert mcq.bodytext == loaded_mcq.bodytext
        assert mcq.imgpath == loaded_mcq.imgpath
        assert mcq.answers == loaded_mcq.answers
        assert mcq.feedbacks == loaded_mcq.feedbacks
        assert mcq.correct_answer == loaded_mcq.correct_answer
