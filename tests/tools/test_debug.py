import pytest
from unittest.mock import patch
from nail.tools.debug.debug_file import debug_file

# Test data
TEST_PROMPT = "Fix any bugs in the file."
TEST_MODIFIED_CONTENT = "def test_function():\n    return 43\n"


@pytest.fixture
def MockFileEditor():
    with patch("nail.tools.debug.debug_file.FileEditor", autospec=True) as mock:
        yield mock


@pytest.fixture
def MockChat():
    with patch("nail.tools.debug.debug_file.Chat", autospec=True) as mock:
        mock_chat = mock.return_value
        mock_chat.predict_code.return_value = TEST_MODIFIED_CONTENT
        yield mock


@pytest.fixture
def MockPrompt():
    with patch("nail.tools.debug.debug_file.DebugPrompt", autospec=True) as mock:
        mock_prompt = mock.return_value
        mock_prompt.text.return_value = TEST_PROMPT
        yield mock


@pytest.mark.parametrize("error_message", [None, "error message"])
def test_debug_file(MockFileEditor, MockChat, MockPrompt, error_message):
    mock_file_editor = MockFileEditor.return_value

    debug_file("test_file.py", error_message)

    mock_file_editor.apply_changes.assert_called_once_with(
        TEST_MODIFIED_CONTENT)
