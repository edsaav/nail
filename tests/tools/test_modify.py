from unittest.mock import patch, ANY
from app.tools.modify.modify_file import modify_file


@patch("app.tools.modify.modify_file.apply_changes")
@patch("app.tools.modify.modify_file.read_file")
@patch("app.tools.modify.modify_file.predict_code")
@patch("app.tools.modify.modify_file.build_context_prefix")
def test_modify_file_with_optional_context_files(mock_build_context_prefix, mock_predict_code, mock_read_file, mock_apply_changes):
    mock_file_content = "This is the original file content."
    mock_request = "Please add a new line at the end."
    mock_modified_content = "This is the modified file content."
    mock_context_file_paths = ["context_file_1", "context_file_2"]
    mock_additional_file_context = "Additional context from files."

    mock_predict_code.return_value = mock_modified_content
    mock_read_file.return_value = mock_file_content
    mock_build_context_prefix.return_value = mock_additional_file_context

    modify_file("dummy_file_path", mock_request,
                context_file_paths=mock_context_file_paths)

    # Assertions
    mock_read_file.assert_called_once_with("dummy_file_path")
    mock_build_context_prefix.assert_called_once_with(mock_context_file_paths)
    mock_predict_code.assert_called_once()
    mock_apply_changes.assert_called_once_with(
        "dummy_file_path", mock_modified_content)


@patch("app.tools.modify.modify_file.apply_changes")
@patch("app.tools.modify.modify_file.read_file")
@patch("app.tools.modify.modify_file.predict_code")
def test_modify_file_without_context_files(mock_predict_code, mock_read_file, mock_apply_changes):
    mock_file_content = "This is the original file content."
    mock_request = "Please add a new line at the end."
    mock_modified_content = "This is the modified file content."

    mock_predict_code.return_value = mock_modified_content
    mock_read_file.return_value = mock_file_content

    modify_file("dummy_file_path", mock_request)

    # Assertions
    mock_read_file.assert_called_once_with("dummy_file_path")
    mock_predict_code.assert_called_once()
    mock_apply_changes.assert_called_once_with(
        "dummy_file_path", mock_modified_content)


@patch("app.tools.modify.modify_file.apply_changes")
@patch("app.tools.modify.modify_file.read_file")
@patch("app.tools.modify.modify_file.predict_code")
def test_modify_file_with_specified_model(mock_predict_code, mock_read_file, mock_apply_changes):
    mock_file_content = "This is the original file content."
    mock_request = "Please add a new line at the end."
    mock_modified_content = "This is the modified file content."
    mock_model = "gpt-4"

    mock_predict_code.return_value = mock_modified_content
    mock_read_file.return_value = mock_file_content

    modify_file("dummy_file_path", mock_request, model=mock_model)

    # Assertions
    mock_read_file.assert_called_once_with("dummy_file_path")
    mock_predict_code.assert_called_once_with(
        ANY, model=mock_model)
    mock_apply_changes.assert_called_once_with(
        "dummy_file_path", mock_modified_content)
