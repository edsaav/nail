import os
import tempfile
import pytest
from unittest.mock import patch, call
from app.core.file_utils import read_file, write_file, open_editor, confirm_diff, apply_changes, print_colored_diff_line


def test_read_file():
    # Create a temporary file with some content
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b"Hello, World!")
        temp_file_path = temp_file.name

    # Test read_file function
    content = read_file(temp_file_path)
    assert content == "Hello, World!"

    # Clean up the temporary file
    os.remove(temp_file_path)


def test_write_file():
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name

    # Test write_file function
    write_file(temp_file_path, "Hello, World!")

    # Check if the content is written correctly
    with open(temp_file_path, "r") as file:
        content = file.read()
    assert content == "Hello, World!"

    # Clean up the temporary file
    os.remove(temp_file_path)


@patch("subprocess.call")
def test_open_editor_default(mock_call):
    file_path = "test.txt"
    open_editor(file_path)
    mock_call.assert_called_once_with(["vim", file_path])


@patch("subprocess.call")
def test_open_editor_with_custom_editor(mock_call):
    # Test with updated EDITOR var
    old_environ = os.environ.copy()
    try:
        os.environ["EDITOR"] = "nano"
        file_path = "test.txt"
        open_editor(file_path)
        mock_call.assert_called_once_with(["nano", file_path])
    finally:
        os.environ.clear()
        os.environ.update(old_environ)


@patch("app.core.file_utils.input")
@patch("app.core.file_utils.read_file")
@patch("app.core.file_utils.print_colored_diff_line")
def test_confirm_diff(mock_print_colored_diff_line, mock_read_file, mock_input):
    # Mock the read_file function to return a fixed content
    mock_read_file.return_value = "Hello, World!"
    # Mock the user input to return 'y' for confirmation
    mock_input.return_value = 'y'

    # Test confirm_diff function
    file_path = "test.txt"
    new_content = "Hello, New World!"
    result = confirm_diff(file_path, new_content)
    assert result == True

    # Assert that print_colored_diff_line is called with the correct diff lines
    expected_calls = [
        call('-Hello, World!'),
        call('+Hello, New World!'),
    ]
    mock_print_colored_diff_line.assert_has_calls(
        expected_calls, any_order=True)

@patch("app.core.file_utils.confirm_diff")
@patch("app.core.file_utils.write_file")
def test_apply_changes(mock_write_file, mock_confirm_diff):
    # Mock the confirm_diff function to return True
    mock_confirm_diff.return_value = True

    # Test apply_changes function
    file_path = "test.txt"
    new_content = "Hello, New World!"
    result = apply_changes(file_path, new_content)
    assert result == True

    # Assert that write_file is called with the correct arguments
    mock_write_file.assert_called_once_with(file_path, new_content)

@patch("app.core.file_utils.confirm_diff")
@patch("app.core.file_utils.write_file")
def test_apply_changes_no_confirmation(mock_write_file, mock_confirm_diff):
    # Mock the confirm_diff function to return False
    mock_confirm_diff.return_value = False

    # Test apply_changes function
    file_path = "test.txt"
    new_content = "Hello, New World!"
    result = apply_changes(file_path, new_content)
    assert result == False

    # Assert that write_file is not called
    mock_write_file.assert_not_called()
