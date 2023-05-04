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
        yield mock


@pytest.fixture
def MockPrompt():
    with patch("nail.tools.build.build_file.BuildPrompt", autospec=True) as mock:
        yield mock


def test_build_file(
    MockFileEditor, MockChat, MockPrompt
):
    mock_file_editor = MockFileEditor()
    mock_chat = MockChat.return_value
    mock_prompt = MockPrompt.return_value
    file_path = "test_file_path"
    mock_chat.predict_code.return_value = "draft_contents"
    mock_prompt.text.return_value = "prompt"

    build_file(file_path)

    # Assertions
    mock_chat.predict_code.assert_called_once_with("prompt")
    mock_file_editor.apply_changes.assert_called_once_with(
        "draft_contents")
