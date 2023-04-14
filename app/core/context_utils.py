from app.core.file_utils import read_file
import os

CONTEXT_PREFIX = "Existing files for context:\n\n"
CONTEXT_SUFFIX = "Given the above context, draft a new file using the following request:\n\n"


def build_context_prefix(context_file_paths):
    """
    Build the context prefix string based on the provided context file paths.

    :param context_file_paths: List of file paths to be used as context
    :return: context_prefix: String containing the context prefix
    """
    context_prefix = ""
    if context_file_paths:
        context_prefix += CONTEXT_PREFIX
        for context_file_path in context_file_paths:
            context_content = read_file(context_file_path)
            context_prefix += format_file_block(
                context_file_path, context_content)
        context_prefix += CONTEXT_SUFFIX
    return context_prefix


def format_file_label(file_path):
    return f"[[{file_path}]]"


def format_file_block(context_file_path, context_content):
    return f"{format_file_label(context_file_path)}\n```\n{context_content}\n```\n\n"


def list_all_files(path=None):
    """
    Recursively list all file paths within the given directory, including files
    nested within sub-directories, ignoring files or directories with names starting with a period.

    :param path: Optional path to the directory. If not provided, uses the current path.
    :return: List of strings containing file paths within the directory.
    """
    if path is None:
        path = os.getcwd()

    file_paths = []

    for root, dirs, files in os.walk(path):
        # Ignore directories starting with a period
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            # Ignore files starting with a period
            if not file.startswith('.'):
                file_paths.append(os.path.join(root, file))

    return file_paths


def build_context_prefix_from_directory(path=None):
    """
    Build the context prefix string based on all the files in the specified (or current) directory.

    :param path: Optional path to the directory. If not provided, uses the current path.
    :return: context_prefix: String containing the context prefix
    """
    context_file_paths = list_all_files(path)
    context_prefix = build_context_prefix(context_file_paths)
    return context_prefix