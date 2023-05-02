import pytest
import tempfile

from pathlib import Path
from nail.core.prompt.context_compiler import ContextCompiler


@pytest.fixture
def temp_files():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        file_names = ["file1.txt", "file2.py", "_hidden.txt", "test_file.py"]
        for file_name in file_names:
            with open(temp_dir_path / file_name, "w") as f:
                f.write("test content")
        yield temp_dir_path


def test_compile_all(temp_files):
    context_compiler = ContextCompiler(context_file_paths=[temp_files])
    result = context_compiler.compile_all()
    assert ContextCompiler.CONTEXT_PREFIX in result
    assert "file1.txt" in result
    assert "file2.py" in result
    assert "_hidden.txt" in result
    assert "test_file.py" in result


def test_compile_all_minus_ignored(temp_files):
    context_compiler = ContextCompiler(context_file_paths=[temp_files])
    result = context_compiler.compile_all_minus_ignored()
    assert ContextCompiler.CONTEXT_PREFIX in result
    assert "file1.txt" in result
    assert "file2.py" in result
    assert "_hidden.txt" not in result
    assert "test_file.py" not in result
