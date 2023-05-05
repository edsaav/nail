import pytest

from unittest.mock import patch
from nail.core.prompt.prompt import (
    BuildPrompt,
    BuildReadmePrompt,
    DebugPrompt,
    ModifyPrompt,
    SpecPrompt,
    BUILD_REQUEST,
    README_REQUEST,
    ERROR_REQUEST,
    RETURN_FULL_FILE,
    ORIGINAL_FILE_TAG,
    REQUEST_TAG,
    SPEC_PREFIX
)

MOCK_LOCAL_CONFIG = {
    "prompt_instructions": {
        "build": "build_instructions",
        "readme": "readme_instructions",
        "debug": "debug_instructions",
        "modify": "modify_instructions",
        "spec": "spec_instructions",
    }
}

FILE_TEXT = "file_text"
CONTEXT_TEXT = "context_file_text"
PARTIAL_CONTEXT_TEXT = "partial_context_file_text"
FILE_BLOCK = "\n```file_text```\n"


@pytest.fixture
def MockFileEditor():
    with patch("nail.core.prompt.prompt.FileEditor", autospec=True) as mock:
        mock_file = mock.return_value
        mock_file.content.return_value = FILE_TEXT
        yield mock


@pytest.fixture
def MockContextCompiler():
    with patch("nail.core.prompt.prompt.ContextCompiler", autospec=True) as mock:
        mock_context = mock.return_value
        mock_context.compile_all.return_value = "context_file_text\n"
        mock_context.compile_all_minus_ignored.return_value = "partial_context_file_text\n"
        yield mock


@pytest.fixture
def mock_file_block():
    with patch("nail.core.prompt.prompt.file_block", autospec=True) as mock:
        mock.return_value = "\n```file_text```\n"
        yield mock


@pytest.fixture
def mock_load_local_config():
    with patch("nail.core.prompt.prompt.load_local_config", autospec=True) as mock:
        mock.return_value = MOCK_LOCAL_CONFIG
        yield mock


def test_build_prompt_text(MockFileEditor, MockContextCompiler, mock_load_local_config):
    build_prompt = BuildPrompt("file_path", ["context_file_path"])
    expected_text = (
        f"{CONTEXT_TEXT}\n"
        f"{BUILD_REQUEST}\n"
        f"{FILE_TEXT}\n"
        "build_instructions"
    )
    assert build_prompt.text() == expected_text


def test_build_readme_prompt_text(MockFileEditor, MockContextCompiler, mock_load_local_config):
    build_readme_prompt = BuildReadmePrompt()
    expected_text = (
        f"{PARTIAL_CONTEXT_TEXT}\n"
        f"{README_REQUEST}\n"
        "readme_instructions"
    )
    assert build_readme_prompt.text() == expected_text


def test_debug_prompt_text(mock_file_block, mock_load_local_config):
    debug_prompt = DebugPrompt("file_path", ["context_file_path"], {
                               "error_message": "error_message"})
    expected_text = (
        f"{FILE_BLOCK}"
        f"{ERROR_REQUEST}\n"
        "error_message\n"
        f"{RETURN_FULL_FILE}\n"
        "debug_instructions"
    )
    assert debug_prompt.text() == expected_text


def test_modify_prompt_text(MockContextCompiler, mock_load_local_config, mock_file_block):
    modify_prompt = ModifyPrompt(
        "file_path", ["context_file_path"], {"request": "request"})
    expected_text = (
        f"{CONTEXT_TEXT}\n"
        f"{ORIGINAL_FILE_TAG}\n"
        f"{FILE_BLOCK}"
        f"{REQUEST_TAG} request\n"
        f"{RETURN_FULL_FILE}\n"
        "modify_instructions"
    )
    assert modify_prompt.text() == expected_text


def test_spec_prompt_text(mock_load_local_config, mock_file_block):
    spec_prompt = SpecPrompt("file_path")
    expected_text = (
        f"{SPEC_PREFIX}\n"
        f"{FILE_BLOCK}\n"
        "spec_instructions"
    )
    assert spec_prompt.text() == expected_text
