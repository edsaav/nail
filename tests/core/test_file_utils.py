import os
import tempfile
import pytest
from app.core.file_utils import read_file, write_file


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


if __name__ == "__main__":
    pytest.main()
