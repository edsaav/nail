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

# Patch decorators
read_file_patch = patch("app.tools.debug.debug_file.read_file", read_file_mock)
write_file_patch = patch(
    "app.tools.debug.debug_file.write_file", write_file_mock)
predict_code_patch = patch(
    "app.tools.debug.debug_file.predict_code", predict_code_mock)


@pytest.mark.parametrize("error_message", [TEST_ERROR_MESSAGE, None])
def test_debug_file(error_message):
    write_file_mock.reset_mock()
    read_file_mock.reset_mock()
    predict_code_mock.reset_mock()

    with read_file_patch, write_file_patch, predict_code_patch:
        debug_file(TEST_FILE_PATH, error_message)

        # Assert read_file is called with the correct file path
        read_file_mock.assert_called_once_with(TEST_FILE_PATH)

        # Assert predict_code is called with the correct prompt
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
        predict_code_mock.assert_called_once_with(expected_prompt)

        # Assert write_file is called with the correct file path and modified contents
        write_file_mock.assert_called_once_with(
            TEST_FILE_PATH, TEST_MODIFIED_CONTENT)
