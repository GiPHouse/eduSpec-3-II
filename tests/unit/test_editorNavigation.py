import importlib
import sys
from types import ModuleType, SimpleNamespace
from typing import Any
from unittest.mock import Mock, mock_open, patch


class DummyContext:
    """Simple context manager used to mock Streamlit forms."""

    def __enter__(self) -> "DummyContext":
        """Enter the context."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: Any,
    ) -> bool:
        """Exit the context without suppressing exceptions."""
        return False


def load_editornavigation_module(
    *,
    question_type: str = "Multiple Choice",
    title: str = "Example Title",
    question_body: str = "Example body",
    uploaded_file: Any = None,
    submit_button: bool = False,
    session_state: dict[str, Any] | None = None,
) -> tuple[ModuleType, dict[str, Any]]:
    """Import editornavigation with patched dependencies and return the module and captured mocks."""
    fake_streamlit = SimpleNamespace()
    fake_streamlit.session_state = {} if session_state is None else session_state

    fake_streamlit.form = Mock(return_value=DummyContext())
    fake_streamlit.selectbox = Mock(return_value=question_type)
    fake_streamlit.text_input = Mock(return_value=title)
    fake_streamlit.text_area = Mock(return_value=question_body)
    fake_streamlit.file_uploader = Mock(return_value=uploaded_file)
    fake_streamlit.form_submit_button = Mock(return_value=submit_button)
    fake_streamlit.error = Mock()
    fake_streamlit.success = Mock()

    fake_create_forms = SimpleNamespace()
    fake_create_forms.decideAndCreateForm = Mock()

    fake_editor = SimpleNamespace()
    fake_editor.QuestionType = [
        SimpleNamespace(typestr="Multiple Choice"),
        SimpleNamespace(typestr="Open"),
        SimpleNamespace(typestr="Molecule"),
    ]
    fake_editor.determine_output_path = Mock(return_value="../data/testfile.dat")

    captured: dict[str, Any] = {
        "st": fake_streamlit,
        "CreateForms": fake_create_forms,
        "editor": fake_editor,
    }

    sys.modules.pop("editornavigation", None)

    with patch.dict(
        sys.modules,
        {
            "streamlit": fake_streamlit,
            "editor.CreateForms": fake_create_forms,
            "editor.editor": fake_editor,
        },
    ):
        module = importlib.import_module("editornavigation")

    return module, captured


def test_form_fields_are_created_with_expected_arguments() -> None:
    """The module should create the expected form fields during import."""
    _, captured = load_editornavigation_module()

    st = captured["st"]

    assert st.form.call_count == 1
    assert st.form.call_args.args == ("baseform",)

    assert st.selectbox.call_count == 1
    assert st.selectbox.call_args.kwargs == {
        "label": "Select the type of the question that you want to create",
        "options": ["Multiple Choice", "Open", "Molecule"],
    }

    assert st.text_input.call_count == 1
    assert st.text_input.call_args.args == ("Title",)
    assert st.text_input.call_args.kwargs == {
        "placeholder": "Put in the title of the question",
        "key": "titlefield",
    }

    assert st.text_area.call_count == 1
    assert st.text_area.call_args.args == ("Question Body",)
    assert st.text_area.call_args.kwargs == {
        "placeholder": "Put in the body of the question",
        "key": "bodyfield",
    }

    assert st.file_uploader.call_count == 1
    assert st.file_uploader.call_args.args == ("Choose a file",)

    assert st.form_submit_button.call_count == 1
    assert st.form_submit_button.call_args.args == ("Next",)


def test_no_submit_and_no_previous_success_does_nothing() -> None:
    """The module should do nothing after the form when not submitted and with no previous success."""
    _, captured = load_editornavigation_module(submit_button=False, session_state={})

    st = captured["st"]
    create_forms = captured["CreateForms"]

    assert st.error.call_count == 0
    assert st.success.call_count == 0
    assert create_forms.decideAndCreateForm.call_count == 0
    assert "last_successful_title" not in st.session_state
    assert "last_successful_questionBody" not in st.session_state
    assert "last_successful_questionType" not in st.session_state


def test_submit_with_missing_title_shows_error() -> None:
    """Submitting with an empty title should show an error."""
    _, captured = load_editornavigation_module(
        title="   ",
        question_body="Valid body",
        submit_button=True,
        session_state={},
    )

    st = captured["st"]
    create_forms = captured["CreateForms"]

    assert st.error.call_count == 1
    assert st.error.call_args.args == ("Title and Question Body are required.",)
    assert st.success.call_count == 0
    assert create_forms.decideAndCreateForm.call_count == 0


def test_submit_with_missing_question_body_shows_error() -> None:
    """Submitting with an empty question body should show an error."""
    _, captured = load_editornavigation_module(
        title="Valid title",
        question_body="   ",
        submit_button=True,
        session_state={},
    )

    st = captured["st"]
    create_forms = captured["CreateForms"]

    assert st.error.call_count == 1
    assert st.error.call_args.args == ("Title and Question Body are required.",)
    assert st.success.call_count == 0
    assert create_forms.decideAndCreateForm.call_count == 0


def test_submit_without_file_saves_form_data_and_creates_next_form() -> None:
    """Submitting valid data without a file should store session state and continue."""
    _, captured = load_editornavigation_module(
        question_type="Open",
        title="My Title",
        question_body="My Body",
        uploaded_file=None,
        submit_button=True,
        session_state={},
    )

    st = captured["st"]
    create_forms = captured["CreateForms"]
    editor = captured["editor"]

    assert st.error.call_count == 0
    assert st.success.call_count == 0
    assert editor.determine_output_path.call_count == 0
    assert st.session_state["last_successful_title"] == "My Title"
    assert st.session_state["last_successful_questionBody"] == "My Body"
    assert st.session_state["last_successful_questionType"] == "Open"
    assert create_forms.decideAndCreateForm.call_count == 1


def test_submit_with_file_saves_uploaded_file_and_updates_session_state() -> None:
    """Submitting valid data with a file should save the file and store its path."""
    uploaded_file = Mock()
    uploaded_file.getbuffer.return_value = b"file-bytes"

    with patch("os.makedirs") as mock_makedirs, patch("builtins.open", mock_open()) as mocked_file:
        _, captured = load_editornavigation_module(
            question_type="Molecule",
            title="Mol Title",
            question_body="Mol Body",
            uploaded_file=uploaded_file,
            submit_button=True,
            session_state={},
        )

    st = captured["st"]
    create_forms = captured["CreateForms"]
    editor = captured["editor"]

    assert mock_makedirs.call_count == 1
    assert mock_makedirs.call_args.args == ("../data",)
    assert mock_makedirs.call_args.kwargs == {"exist_ok": True}

    assert editor.determine_output_path.call_count == 1
    assert editor.determine_output_path.call_args.args == (uploaded_file,)

    mocked_file.assert_called_once_with("../data/testfile.dat", "wb")
    mocked_file().write.assert_called_once_with(b"file-bytes")

    assert st.success.call_count == 1
    assert st.success.call_args.args == ("File saved to ../data/testfile.dat",)

    assert st.session_state["last_successful_file"] == "../data/testfile.dat"
    assert st.session_state["last_successful_title"] == "Mol Title"
    assert st.session_state["last_successful_questionBody"] == "Mol Body"
    assert st.session_state["last_successful_questionType"] == "Molecule"

    assert create_forms.decideAndCreateForm.call_count == 1


def test_existing_last_successful_title_replays_validation_logic() -> None:
    """Existing successful state should trigger the post-form logic even without submit."""
    session_state = {"last_successful_title": "Previous Title"}

    _, captured = load_editornavigation_module(
        title="   ",
        question_body="Still filled",
        submit_button=False,
        session_state=session_state,
    )

    st = captured["st"]
    create_forms = captured["CreateForms"]

    assert st.error.call_count == 1
    assert st.error.call_args.args == ("Title and Question Body are required.",)
    assert create_forms.decideAndCreateForm.call_count == 0


def test_existing_last_successful_title_with_valid_data_continues() -> None:
    """Existing successful state with valid current data should continue to the next form."""
    session_state = {"last_successful_title": "Previous Title"}

    _, captured = load_editornavigation_module(
        question_type="Multiple Choice",
        title="Fresh Title",
        question_body="Fresh Body",
        submit_button=False,
        session_state=session_state,
    )

    st = captured["st"]
    create_forms = captured["CreateForms"]

    assert st.error.call_count == 0
    assert st.session_state["last_successful_title"] == "Fresh Title"
    assert st.session_state["last_successful_questionBody"] == "Fresh Body"
    assert st.session_state["last_successful_questionType"] == "Multiple Choice"
    assert create_forms.decideAndCreateForm.call_count == 1
