import pytest
from unittest.mock import patch
from nail.tools.build.build_file import build_file


@pytest.fixture
def MockFileEditor():
    with patch("nail.tools.build.build_file.FileEditor", autospec=True) as mock:
        yield mock


@pytest.fixture
def MockContextCompiler():
    with patch("nail.tools.build.build_file.ContextCompiler", autospec=True) as mock:
        yield mock


@pytest.fixture
def mock_predict_code():
    with patch("nail.tools.build.build_file.predict_code", autospec=True) as mock:
        yield mock


def test_build_file_no_context(
    MockFileEditor, MockContextCompiler, mock_predict_code
):
    mock_file_editor = MockFileEditor()
    mock_context_compiler = MockContextCompiler.return_value
    file_path = "test_file_path"
    mock_file_editor.content.return_value = "prompt"
    mock_context_compiler.compile_all.return_value = ""
    mock_predict_code.return_value = "draft_contents"

    build_file(file_path)

    # Assertions
    mock_file_editor.content.assert_called_once()
    mock_context_compiler.compile_all.assert_called_once()
    mock_predict_code.assert_called_once_with("prompt", model=None)
    mock_file_editor.apply_changes.assert_called_once_with(
        "draft_contents")


def test_build_file_with_context(
    MockFileEditor, MockContextCompiler, mock_predict_code
):
    mock_file_editor = MockFileEditor()
    mock_context_compiler = MockContextCompiler.return_value
    file_path = "test_file_path"
    context_file_paths = ["context1", "context2"]
    mock_file_editor.content.return_value = "prompt"
    mock_context_compiler.compile_all.return_value = "context_prefix"
    mock_predict_code.return_value = "draft_contents"

    build_file(file_path, context_file_paths)

    # Assertions
    mock_file_editor.content.assert_called_once()
    mock_context_compiler.compile_all.assert_called_once()
    mock_predict_code.assert_called_once_with(
        "context_prefixprompt", model=None)
    mock_file_editor.apply_changes.assert_called_once_with("draft_contents")


def test_build_file_with_model(
    MockFileEditor, MockContextCompiler, mock_predict_code
):
    mock_file_editor = MockFileEditor()
    mock_context_compiler = MockContextCompiler.return_value
    file_path = "test_file_path"
    context_file_paths = ["context1", "context2"]
    mock_file_editor.content.return_value = "prompt"
    mock_context_compiler.compile_all.return_value = "context_prefix"
    mock_predict_code.return_value = "draft_contents"

    build_file(file_path, context_file_paths, model="gpt-4")

    # Assertions
    mock_file_editor.content.assert_called_once()
    mock_context_compiler.compile_all.assert_called_once()
    mock_predict_code.assert_called_once_with(
        "context_prefixprompt", model="gpt-4")
    mock_file_editor.apply_changes.assert_called_once_with("draft_contents")
