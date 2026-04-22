import pathlib

import pytest
from streamlit import cache_data

from managers.BaseManager import BaseManager
from managers.QuestionManager import QuestionManager
from managers.QuestionSerialiser import QuestionSerialiser
from questions.MultipleChoiceQuestion import MultipleChoiceQuestion


class TestQuestionManager:
    """Test cases for the question manager"""

    def test_SaveLocation(self, tmp_path: pathlib.Path) -> None:
        """Test case for changing the question manager's save location"""
        BaseManager._data_dir = tmp_path  # noqa: SLF001

        assert QuestionManager._getDir() == tmp_path.joinpath(QuestionManager._item_dir)  # noqa: SLF001

    def test_SavingMCQ(self, tmp_path: pathlib.Path) -> None:
        """Test case for saving a multiple-choice question"""
        BaseManager._data_dir = tmp_path  # noqa: SLF001
        cache_data.clear()

        mcq = MultipleChoiceQuestion(
            "question1",
            "Example Question",
            "here's a question",
            ["a", "b", "c"],
            1,
            ["a: wrong", "b: correct", "c: wrong"],
        )

        assert QuestionManager.saveQuestion(mcq)

        # The ruff comment here hurts me more than it hurts you, trust me
        expected_location = tmp_path.joinpath(QuestionManager._item_dir).joinpath(  # noqa: SLF001
            f"{mcq.name}.json"
        )

        assert expected_location.is_file()

        saved_data = expected_location.read_text()

        assert saved_data == QuestionSerialiser.questionToJson(mcq)

    def test_LoadMCQ(self, tmp_path: pathlib.Path) -> None:
        """Test case for loading a multiple-choice question"""
        BaseManager._data_dir = tmp_path  # noqa: SLF001
        cache_data.clear()

        location = tmp_path.joinpath(QuestionManager._item_dir).joinpath("question1.json")  # noqa: SLF001
        location.parent.mkdir(exist_ok=True)
        location.touch()
        location.write_text(
            r"""{"id": "question1", "title": "Example Question", "bodyText": "here's a question", "imagePath": [], "version": 1, "type": "multipleChoice", "answers": ["a", "b", "c"], "correctAnswer": 1, "feedbacks": ["a: wrong", "b: correct", "c: wrong"]}"""
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
        BaseManager._data_dir = tmp_path  # noqa: SLF001
        cache_data.clear()

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

    def test_UpdateMCQ(self, tmp_path: pathlib.Path) -> None:
        """Test case for updating a multiple-choice question"""
        BaseManager._data_dir = tmp_path  # noqa: SLF001
        cache_data.clear()

        mcq_1 = MultipleChoiceQuestion(
            "question1",
            "Example Question",
            "here's a question",
            ["a", "b", "c"],
            1,
            ["a: wrong", "b: correct", "c: wrong"],
        )

        mcq_2 = MultipleChoiceQuestion(
            "question1",
            "Example Update",
            "here's an updated question",
            ["1", "2", "3"],
            0,
            ["1: correct", "2: wrong", "3: wrong"],
            imgpath=["data/img/test1"],
        )

        assert QuestionManager.saveQuestion(mcq_1)

        assert QuestionManager.updateQuestion(mcq_2)

        loaded_mcq = QuestionManager.loadQuestion("question1")

        assert isinstance(loaded_mcq, MultipleChoiceQuestion)

        assert mcq_2.name == loaded_mcq.name
        assert mcq_2.title == loaded_mcq.title
        assert mcq_2.bodytext == loaded_mcq.bodytext
        assert mcq_2.imgpath == loaded_mcq.imgpath
        assert mcq_2.answers == loaded_mcq.answers
        assert mcq_2.feedbacks == loaded_mcq.feedbacks
        assert mcq_2.correct_answer == loaded_mcq.correct_answer

    def test_LoadMCQ_nonexistent(self, tmp_path: pathlib.Path) -> None:
        """Test case for loading a non-existent multiple-choice question"""
        BaseManager._data_dir = tmp_path  # noqa: SLF001
        cache_data.clear()

        expected_location = tmp_path.joinpath("doesnotexist.json")

        assert not expected_location.exists()

        with pytest.raises(FileNotFoundError):
            assert None is QuestionManager.loadQuestion("doesnotexist")

    def test_SaveMCQ_duplicate(self, tmp_path: pathlib.Path) -> None:
        """Test case for saving a multiple-choice question twice"""
        BaseManager._data_dir = tmp_path  # noqa: SLF001
        cache_data.clear()

        mcq = MultipleChoiceQuestion(
            "question1",
            "Example Question",
            "here's a question",
            ["a", "b", "c"],
            1,
            ["a: wrong", "b: correct", "c: wrong"],
        )

        assert QuestionManager.saveQuestion(mcq)

        with pytest.raises(FileExistsError):
            assert not QuestionManager.saveQuestion(mcq)

    def test_UpdateMCQ_nonexistent(self, tmp_path: pathlib.Path) -> None:
        """Test case for updating a non-existent multiple-choice question"""
        BaseManager._data_dir = tmp_path  # noqa: SLF001
        cache_data.clear()

        expected_location = tmp_path.joinpath("doesnotexist.json")

        assert not expected_location.exists()

        mcq = MultipleChoiceQuestion(
            "question1",
            "Example Question",
            "here's a question",
            ["a", "b", "c"],
            1,
            ["a: wrong", "b: correct", "c: wrong"],
        )

        with pytest.raises(FileNotFoundError):
            assert not QuestionManager.updateQuestion(mcq)

    def test_CycleMCQ_multiple(self, tmp_path: pathlib.Path) -> None:
        """Test case for cycling multiple multiple-choice questions"""
        BaseManager._data_dir = tmp_path  # noqa: SLF001
        cache_data.clear()

        mcq_1 = MultipleChoiceQuestion(
            "question1",
            "Example Question",
            "here's a question",
            ["a", "b", "c"],
            1,
            ["a: wrong", "b: correct", "c: wrong"],
        )

        mcq_2 = MultipleChoiceQuestion(
            "question2",
            "Example Update",
            "here's an updated question",
            ["1", "2", "3"],
            0,
            ["1: correct", "2: wrong", "3: wrong"],
            imgpath=["data/img/test1"],
        )

        mcq_3 = MultipleChoiceQuestion(
            "question3",
            "Title 3",
            "third question",
            [
                "true",
                "false",
            ],
            1,
            ["true: false", "false: true"],
        )

        assert QuestionManager.saveQuestion(mcq_1)
        assert QuestionManager.saveQuestion(mcq_2)
        assert QuestionManager.saveQuestion(mcq_3)

        loaded_mcq_1 = QuestionManager.loadQuestion("question1")
        loaded_mcq_2 = QuestionManager.loadQuestion("question2")
        loaded_mcq_3 = QuestionManager.loadQuestion("question3")

        assert isinstance(loaded_mcq_1, MultipleChoiceQuestion)
        assert isinstance(loaded_mcq_2, MultipleChoiceQuestion)
        assert isinstance(loaded_mcq_3, MultipleChoiceQuestion)

        assert mcq_1.name == loaded_mcq_1.name
        assert mcq_1.title == loaded_mcq_1.title
        assert mcq_1.bodytext == loaded_mcq_1.bodytext
        assert mcq_1.imgpath == loaded_mcq_1.imgpath
        assert mcq_1.answers == loaded_mcq_1.answers
        assert mcq_1.feedbacks == loaded_mcq_1.feedbacks
        assert mcq_1.correct_answer == loaded_mcq_1.correct_answer

        assert mcq_2.name == loaded_mcq_2.name
        assert mcq_2.title == loaded_mcq_2.title
        assert mcq_2.bodytext == loaded_mcq_2.bodytext
        assert mcq_2.imgpath == loaded_mcq_2.imgpath
        assert mcq_2.answers == loaded_mcq_2.answers
        assert mcq_2.feedbacks == loaded_mcq_2.feedbacks
        assert mcq_2.correct_answer == loaded_mcq_2.correct_answer

        assert mcq_3.name == loaded_mcq_3.name
        assert mcq_3.title == loaded_mcq_3.title
        assert mcq_3.bodytext == loaded_mcq_3.bodytext
        assert mcq_3.imgpath == loaded_mcq_3.imgpath
        assert mcq_3.answers == loaded_mcq_3.answers
        assert mcq_3.feedbacks == loaded_mcq_3.feedbacks
        assert mcq_3.correct_answer == loaded_mcq_3.correct_answer
