import pytest
from unittest.mock import patch
from nail.tools.build.build_file import build_file


@pytest.fixture
def MockFileEditor():
    with patch("nail.tools.build.build_file.FileEditor", autospec=True) as mock:
        yield mock


@pytest.fixture
def MockChat():
    with patch("nail.tools.build.build_file.Chat", autospec=True) as mock:
        mock_chat = mock.return_value
        mock_chat.predict_code.return_value = "draft_contents"
        yield mock


@pytest.fixture
def MockPrompt():
    with patch("nail.tools.build.build_file.BuildPrompt", autospec=True) as mock:
        mock_prompt = mock.return_value
        mock_prompt.text.return_value = "prompt"
        yield mock


def test_build_file(MockFileEditor, MockChat, MockPrompt):
    mock_file_editor = MockFileEditor.return_value

    build_file("test_file_path")

    mock_file_editor.apply_changes.assert_called_once_with("draft_contents")


@patch("nail.tools.build.build_file.FileEditor", autospec=True)
def test_build_file_no_file(MockFileEditor, MockChat, MockPrompt):
    mock_file_editor = MockFileEditor.return_value
    mock_file_editor.exists.return_value = False

    build_file("test_file_path", context_file_paths=None)

    mock_file_editor.open_editor.assert_called_once()
    mock_file_editor.apply_changes.assert_called_once_with("draft_contents")
