import os
import re

from pathlib import Path
from typing import List
from nail.core.prompt.formatting_utils import file_block


class ContextCompiler:
    """
    Compiles prompt context from the files in the given context_file_paths.

    :param context_file_paths: A list of file paths to include in the context.
    :param ignore_list: A list of file names or regex patterns to ignore.
    """
    CONTEXT_PREFIX = "Existing files for context:"
    # TODO: Make this list configurable
    DEFAULT_IGNORE_LIST = ["README", "LICENSE", "^[._]", "^test", "test$"]

    def __init__(self, context_file_paths=[os.getcwd()],
                 ignore_list=DEFAULT_IGNORE_LIST):
        self.context_file_paths = context_file_paths
        self.ignore_list = ignore_list

    def compile_all(self):
        """
        Compiles prompt context from all files in the given context_file_paths.
        This includes a prefix explaining the context, and a code block
        and file name label for each file.

        :return: A string containing the prompt context.
        """
        all_files = self._list_all_files()
        return self._compile_context(all_files)

    def compile_all_minus_ignored(self):
        """
        Compiles prompt context from given context_file_paths. Includes all
        files in the given paths, minus any that are included in the
        ContextCompiler's ignore_list. Context includes a prefix explaining the
        context, and a code block and file name label for each file.

        :return: A string containing the prompt context.
        """
        relevant_files = self._filter_ignored(self._list_all_files())
        return self._compile_context(relevant_files)

    def _compile_context(self, files):
        context = [file_block(file) for file in files]
        return f"{self.CONTEXT_PREFIX}\n\n{''.join(context)}"

    def _list_all_files(self):
        all_file_paths = []
        for path in self.context_file_paths:
            file_paths = self._list_files_at_path(path)
            all_file_paths.extend(file_paths)
        return all_file_paths

    def _list_files_at_path(self, path):
        if os.path.isfile(path):
            return [path]
        file_paths = []
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                file_paths.append(os.path.join(root, file))
        return file_paths

    def _filter_ignored(self, file_paths):
        return [file_path for file_path in file_paths
                if not self._is_ignored(file_path)]

    def _is_ignored(self, file_path):
        # Generate regexes for each item in the ignore list and
        # return True if any of them match the given file path
        file = os.path.basename(file_path)
        return any(re.compile(item).search(file) for item in self.ignore_list)
