from unittest.mock import patch
from nail.tools.spec.build_spec_file import build_spec_file


@patch("nail.tools.spec.build_spec_file.Chat")
@patch("nail.tools.spec.build_spec_file.FileEditor")
def test_build_spec_file(MockFileEditor, MockChat):
    mock_file_editor = MockFileEditor.return_value
    mock_file_editor.content.return_value = "def add(a, b):\n    return a + b"

    mock_chat = MockChat.return_value
    mock_chat.predict_code.return_value = (
        "def test_add():\n"
        "    assert add(1, 2) == 3\n"
    )

    build_spec_file("initial_file.py", "test_initial_file.py")

    # Assertions
    mock_chat.predict_code.assert_called_once_with(
        "Create a unit test file for the following code, using pytest:\n\n```\ndef add(a, b):\n    return a + b\n```",
    )
    mock_file_editor.apply_changes.assert_called_once_with(
        "def test_add():\n    assert add(1, 2) == 3\n")
