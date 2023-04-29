import pytest
from unittest.mock import patch
from nail.tools.build.build_file import build_file


@pytest.fixture
def mock_read_file():
    with patch("nail.tools.build.build_file.read_file", autospec=True) as mock:
        yield mock


@pytest.fixture
def mock_apply_changes():
    with patch("nail.tools.build.build_file.apply_changes", autospec=True) as mock:
        yield mock


@pytest.fixture
def mock_predict_code():
    with patch("nail.tools.build.build_file.predict_code", autospec=True) as mock:
        yield mock


@pytest.fixture
def mock_build_context_prefix():
    with patch("nail.tools.build.build_file.build_context_prefix", autospec=True) as mock:
        yield mock


def test_build_file_no_context(
    mock_read_file, mock_apply_changes, mock_predict_code, mock_build_context_prefix
):
    file_path = "test_file_path"
    mock_read_file.return_value = "prompt"
    mock_build_context_prefix.return_value = ""
    mock_predict_code.return_value = "draft_contents"

    build_file(file_path)

    # Assertions
    mock_read_file.assert_called_once_with(file_path)
    mock_build_context_prefix.assert_called_once_with(None)
    mock_predict_code.assert_called_once_with("prompt", model=None)
    mock_apply_changes.assert_called_once_with(file_path, "draft_contents")


def test_build_file_with_context(
    mock_read_file, mock_apply_changes, mock_predict_code, mock_build_context_prefix
):
    file_path = "test_file_path"
    context_file_paths = ["context1", "context2"]
    mock_read_file.return_value = "prompt"
    mock_build_context_prefix.return_value = "context_prefix"
    mock_predict_code.return_value = "draft_contents"

    build_file(file_path, context_file_paths)

    # Assertions
    mock_read_file.assert_called_once_with(file_path)
    mock_build_context_prefix.assert_called_once_with(context_file_paths)
    mock_predict_code.assert_called_once_with(
        "context_prefixprompt", model=None)
    mock_apply_changes.assert_called_once_with(file_path, "draft_contents")


def test_build_file_with_model(
    mock_read_file, mock_apply_changes, mock_predict_code, mock_build_context_prefix
):
    file_path = "test_file_path"
    context_file_paths = ["context1", "context2"]
    mock_read_file.return_value = "prompt"
    mock_build_context_prefix.return_value = "context_prefix"
    mock_predict_code.return_value = "draft_contents"

    build_file(file_path, context_file_paths, model="gpt-4")

    # Assertions
    mock_read_file.assert_called_once_with(file_path)
    mock_build_context_prefix.assert_called_once_with(context_file_paths)
    mock_predict_code.assert_called_once_with(
        "context_prefixprompt", model="gpt-4")
    mock_apply_changes.assert_called_once_with(file_path, "draft_contents")
