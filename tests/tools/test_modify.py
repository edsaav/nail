from unittest.mock import patch
from app.tools.modify.modify_file import modify_file


@patch("app.tools.modify.modify_file.write_file")
@patch("app.tools.modify.modify_file.read_file")
@patch("app.tools.modify.modify_file.predict_code")
def test_modify_file(mock_predict_code, mock_read_file, mock_write_file):
    mock_file_content = "This is the original file content."
    mock_request = "Please add a new line at the end."
    mock_modified_content = "This is the modified file content."

    mock_predict_code.return_value = mock_modified_content
    mock_read_file.return_value = mock_file_content

    modify_file("dummy_file_path", mock_request)

    # Assertions
    mock_read_file.assert_called_once_with("dummy_file_path")
    mock_predict_code.assert_called_once()
    mock_write_file.assert_called_once_with(
        "dummy_file_path", mock_modified_content)
