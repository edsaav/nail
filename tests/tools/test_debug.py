import pytest
from unittest.mock import MagicMock, patch
from app.tools.debug.debug_file import debug_file

# Test data
TEST_FILE_PATH = "test_file.py"
TEST_FILE_CONTENT = "def test_function():\n    return 42\n"
TEST_ERROR_MESSAGE = "SyntaxError: invalid syntax"
TEST_MODIFIED_CONTENT = "def test_function():\n    return 43\n"

# Mock functions
read_file_mock = MagicMock(return_value=TEST_FILE_CONTENT)
write_file_mock = MagicMock()
predict_code_mock = MagicMock(return_value=TEST_MODIFIED_CONTENT)


@pytest.mark.parametrize("error_message", [TEST_ERROR_MESSAGE, None])
@patch("app.tools.debug.debug_file.write_file", write_file_mock)
@patch("app.tools.debug.debug_file.read_file", read_file_mock)
@patch("app.tools.debug.debug_file.predict_code", predict_code_mock)
def test_debug_file(error_message):
    write_file_mock.reset_mock()
    read_file_mock.reset_mock()
    predict_code_mock.reset_mock()

    expected_request = (
        f"Fix the following error message: {TEST_ERROR_MESSAGE}"
        if error_message
        else "Fix any bugs in the file."
    )
    expected_prompt = (
        f"Original file contents:\n```\n{TEST_FILE_CONTENT}\n```\n\n"
        f"{expected_request}\n"
        "Return the full modified file contents. Any non-code text should only be included as inline comments."
    )

    debug_file(TEST_FILE_PATH, error_message)

    # Assertions
    read_file_mock.assert_called_once_with(TEST_FILE_PATH)
    predict_code_mock.assert_called_once_with(expected_prompt, model=None)
    write_file_mock.assert_called_once_with(
        TEST_FILE_PATH, TEST_MODIFIED_CONTENT)
