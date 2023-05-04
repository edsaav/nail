from unittest.mock import patch
from nail.tools.modify.modify_file import modify_file


@patch("nail.tools.modify.modify_file.Chat")
@patch('nail.tools.modify.modify_file.FileEditor')
@patch("nail.tools.modify.modify_file.ModifyPrompt")
def test_modify_file(MockModifyPrompt, MockFileEditor, MockChat):
    mock_file_editor = MockFileEditor.return_value
    mock_prompt = MockModifyPrompt.return_value
    mock_chat = MockChat.return_value

    # Set the return values for mock functions
    mock_file_editor.content.return_value = 'original content'
    mock_chat.predict_code.return_value = 'expected modified content'
    mock_prompt.text.return_value = 'prompt'

    # Call the modify_file function with the mocked instance
    modify_file('path/to/file', 'request', context_file_paths=None, model=None)

    # Assert the expected behavior
    mock_file_editor.apply_changes.assert_called_once_with(
        'expected modified content')
