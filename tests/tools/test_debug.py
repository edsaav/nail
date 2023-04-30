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


@pytest.mark.parametrize("error_message", [TEST_ERROR_MESSAGE, None])
@patch("nail.tools.debug.debug_file.predict_code", predict_code_mock)
def test_debug_file(error_message, MockFileEditor):
    mock_file_editor = MockFileEditor()
    mock_file_editor.content.return_value = TEST_FILE_CONTENT
    predict_code_mock.reset_mock()

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
    predict_code_mock.assert_called_once_with(expected_prompt, model=None)
    mock_file_editor.apply_changes.assert_called_once_with(
        TEST_MODIFIED_CONTENT)
