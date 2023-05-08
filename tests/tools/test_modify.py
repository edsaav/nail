import pytest

from unittest.mock import patch
from nail.tools.modify.modify_file import modify_file


@pytest.fixture
def MockModifyPrompt():
    with patch("nail.tools.modify.modify_file.ModifyPrompt", autospec=True) as mock:
        yield mock


@pytest.fixture
def MockFileEditor():
    with patch("nail.tools.modify.modify_file.FileEditor", autospec=True) as mock:
        yield mock


@pytest.fixture
def MockChat():
    with patch("nail.tools.modify.modify_file.Chat", autospec=True) as mock:
        mock_chat = mock.return_value
        mock_chat.predict_code.return_value = "expected modified content"
        yield mock


def test_modify_file(MockModifyPrompt, MockFileEditor, MockChat):
    mock_file_editor = MockFileEditor.return_value

    modify_file('path/to/file', 'request', context_file_paths=None, model=None)

    mock_file_editor.apply_changes.assert_called_once_with(
        'expected modified content')
