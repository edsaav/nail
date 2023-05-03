import pytest
from unittest.mock import MagicMock, patch
from nail.tools.debug.debug_file import debug_file

# Test data
TEST_FILE_PATH = "test_file.py"
TEST_FILE_CONTENT = "def test_function():\n    return 42\n"
TEST_ERROR_MESSAGE = "SyntaxError: invalid syntax"
TEST_MODIFIED_CONTENT = "def test_function():\n    return 43\n"

# Mock functions
predict_code_mock = MagicMock(return_value=TEST_MODIFIED_CONTENT)


@pytest.fixture
def MockFileEditor():
    with patch("nail.tools.debug.debug_file.FileEditor", autospec=True) as mock:
        yield mock


@pytest.fixture
def MockChat():
    with patch("nail.tools.debug.debug_file.Chat", autospec=True) as mock:
        yield mock


@pytest.mark.parametrize("error_message", [TEST_ERROR_MESSAGE, None])
def test_debug_file(error_message, MockFileEditor, MockChat):
    mock_file_editor = MockFileEditor.return_value
    mock_chat = MockChat.return_value
    mock_chat.predict_code.return_value = TEST_MODIFIED_CONTENT
    mock_file_editor.content.return_value = TEST_FILE_CONTENT

    expected_request = (
        f"Fix the following error message: {TEST_ERROR_MESSAGE}"
        if error_message
        else "Fix any bugs in the file."
    )
    expected_prompt = (
        f"Original file contents:\n```\n{TEST_FILE_CONTENT}\n```\n\n"
        f"{expected_request}\n"
        "Return the full modified file contents. Any non-code text should "
        + "only be included as inline comments."
    )

    debug_file(TEST_FILE_PATH, error_message)

    # Assertions
    mock_file_editor.content.assert_called_once()
    mock_chat.predict_code.assert_called_once_with(expected_prompt)
    mock_file_editor.apply_changes.assert_called_once_with(
        TEST_MODIFIED_CONTENT)
