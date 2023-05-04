from abc import ABC, abstractmethod

from nail.core.file_editor import FileEditor
from nail.core.prompt.context_compiler import ContextCompiler
from nail.core.prompt.formatting_utils import file_block

ERROR_REQUEST = "Fix the following error message:"
GENERAL_DEBUG_REQUEST = "Fix any bugs in the file."
ORIGINAL_FILE_TAG = "Original file contents:"
README_REQUEST = "Generate a README file for the application."
REQUEST_TAG = "Request:"
RETURN_FULL_FILE = "Return the full modified file contents. Any non-code" \
    + " text should only be included as inline comments."
SPEC_PREFIX = "Create a unit test file for the following code:"


class BasePrompt(ABC):
    """
    Base class for all prompts. Contains common functionality for all prompts.
    All prompts should implement the text method.

    :param file_path: Path to the main file to be edited, debugged, etc
    :param context_file_paths: Paths to other relevant files for context
    :param details: A dictionary of details to be used by specific prompts
    """

    def __init__(self, file_path=None, context_file_paths=None, details=None):
        self.file_path = file_path
        self.context_file_paths = context_file_paths
        self.details = details

    @property
    def _context_text(self):
        if not self.context_file_paths:
            return ""
        return ContextCompiler(self.context_file_paths).compile_all()

    @property
    def _file_text(self):
        FileEditor(self.file_path).content()

    @abstractmethod
    def text(self):
        pass


class BuildPrompt(BasePrompt):
    def text(self):
        return self._context_text + self._file_text


class BuildReadmePrompt(BasePrompt):
    def text(self):
        return self._context_text + README_REQUEST

    @property
    def _context_text(self):
        return ContextCompiler().compile_all_minus_ignored()


class DebugPrompt(BasePrompt):
    def text(self):
        return file_block(self.file_path) \
            + f"\n\n{self._debug_request}\n" \
            + RETURN_FULL_FILE

    @property
    def _debug_request(self):
        error_message = self.details.get("error_message")
        if error_message:
            return f"{ERROR_REQUEST} {error_message}"
        else:
            return GENERAL_DEBUG_REQUEST


class ModifyPrompt(BasePrompt):
    def text(self):
        file_context = f"{ORIGINAL_FILE_TAG}\n{file_block(self.file_path)}"
        additional_file_context = self._context_text
        return additional_file_context + file_context + self._modify_request

    @property
    def _modify_request(self):
        request = self.details.get("request")
        return f"{REQUEST_TAG} {request}\n{RETURN_FULL_FILE}"


class SpecPrompt(BasePrompt):
    def text(self):
        return f"{SPEC_PREFIX}\n\n{file_block(self.file_path)}"
