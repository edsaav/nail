from abc import ABC, abstractmethod

from nail.core.file_editor import FileEditor
from nail.core.prompt.context_compiler import ContextCompiler
from nail.core.prompt.formatting_utils import file_block
from nail.core.config.local_config_utils import load_local_config

BUILD_REQUEST = "Write code to the following specification:"
ERROR_REQUEST = "Fix the following error message:"
EXPLAIN_PREFIX = "Explain the following code:"
GENERAL_DEBUG_REQUEST = "Fix any bugs in the file."
ORIGINAL_FILE_TAG = "Original file contents:"
README_REQUEST = "Generate a README file for the application."
REQUEST_TAG = "Request:"
RETURN_FULL_FILE = (
    "Return the full modified file contents. Any non-code"
    + " text should only be included as inline comments."
)
SPEC_PREFIX = "Create a unit test file for the following code:"
LOW_VERBOSITY = "Keep your answer succinct and to the point."
HIGH_VERBOSITY = "Include a high level of detail."


class BasePrompt(ABC):
    """
    Base class for all prompts. Contains common functionality for all prompts.
    All prompts should implement the text method.

    :param file_path: Path to the main file to be edited, debugged, etc
    :param context_file_paths: Paths to other relevant files for context
    :param details: A dictionary of details to be used by specific prompts
    """

    def __init__(self, file_path=None, context_file_paths=[], details={}):
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
        return FileEditor(self.file_path).content()

    def _custom_instructions(self, key):
        instruction = load_local_config().get("prompt_instructions", {}).get(key)
        return "" if not instruction else f"\n{instruction}"

    @abstractmethod
    def text(self):
        pass


class BuildPrompt(BasePrompt):
    def text(self):
        return (
            self._context_text
            + f"{BUILD_REQUEST}\n"
            + self._file_text
            + self._custom_instructions("build")
        )


class BuildReadmePrompt(BasePrompt):
    def text(self):
        return self._context_text + README_REQUEST + self._custom_instructions("readme")

    @property
    def _context_text(self):
        return ContextCompiler().compile_all_minus_ignored()


class DebugPrompt(BasePrompt):
    def text(self):
        return (
            file_block(self.file_path)
            + f"{self._debug_request}\n"
            + RETURN_FULL_FILE
            + self._custom_instructions("debug")
        )

    @property
    def _debug_request(self):
        error_message = self.details.get("error_message")
        if error_message:
            return f"{ERROR_REQUEST}\n{error_message}"
        else:
            return GENERAL_DEBUG_REQUEST


class ModifyPrompt(BasePrompt):
    def text(self):
        file_context = f"{ORIGINAL_FILE_TAG}\n{file_block(self.file_path)}"
        return (
            self._context_text
            + file_context
            + self._modify_request
            + self._custom_instructions("modify")
        )

    @property
    def _modify_request(self):
        request = self.details.get("request")
        return f"{REQUEST_TAG} {request}\n{RETURN_FULL_FILE}"


class SpecPrompt(BasePrompt):
    def text(self):
        return (
            f"{SPEC_PREFIX}\n{file_block(self.file_path)}"
            + self._custom_instructions("spec")
        )


class ExplainPrompt(BasePrompt):
    def text(self):
        if self.details.get("verbose") is True:
            verbosity = HIGH_VERBOSITY
        else:
            verbosity = LOW_VERBOSITY
        return (
            self._context_text
            + f"{EXPLAIN_PREFIX}\n{file_block(self.file_path)}"
            + verbosity
            + self._custom_instructions("explain")
        )
