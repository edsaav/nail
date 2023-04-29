import pytest
from unittest.mock import patch
from nail.tools.spec.build_spec_file import build_spec_file


@patch("nail.tools.spec.build_spec_file.predict_code")
@patch("nail.tools.spec.build_spec_file.apply_changes")
@patch("nail.tools.spec.build_spec_file.read_file")
def test_build_spec_file(mock_read_file, mock_apply_changes, mock_predict_code):
    mock_read_file.return_value = "def add(a, b):\n    return a + b"

    mock_predict_code.return_value = (
        "def test_add():\n"
        "    assert add(1, 2) == 3\n"
    )

    build_spec_file("initial_file.py", "test_initial_file.py")

    # Assertions
    mock_read_file.assert_called_once_with("initial_file.py")
    mock_predict_code.assert_called_once_with(
        "Create a unit test file for the following code, using pytest:\n\n```\ndef add(a, b):\n    return a + b\n```",
        model=None
    )
    mock_apply_changes.assert_called_once_with(
        "test_initial_file.py", "def test_add():\n    assert add(1, 2) == 3\n")


@patch("nail.tools.spec.build_spec_file.predict_code")
@patch("nail.tools.spec.build_spec_file.apply_changes")
@patch("nail.tools.spec.build_spec_file.read_file")
def test_build_spec_file_with_model(mock_read_file, mock_apply_changes, mock_predict_code):
    mock_read_file.return_value = "def add(a, b):\n    return a + b"

    mock_predict_code.return_value = (
        "def test_add():\n"
        "    assert add(1, 2) == 3\n"
    )

    build_spec_file("initial_file.py", "test_initial_file.py", model="gpt-4")

    # Assertions
    mock_read_file.assert_called_once_with("initial_file.py")
    mock_predict_code.assert_called_once_with(
        "Create a unit test file for the following code, using pytest:\n\n```\ndef add(a, b):\n    return a + b\n```",
        model="gpt-4"
    )
    mock_apply_changes.assert_called_once_with(
        "test_initial_file.py", "def test_add():\n    assert add(1, 2) == 3\n")


if __name__ == "__main__":
    pytest.main()
