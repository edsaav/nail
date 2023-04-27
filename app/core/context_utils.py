from app.core.file_utils import read_file
import os

CONTEXT_PREFIX = "Existing files for context:\n\n"
CONTEXT_SUFFIX = "Given the above context, draft a new file using " \
    + "the following request:\n\n"


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
    label = format_file_label(context_file_path)
    formatted_file_content = f"```\n{context_content}\n```"
    return f"{label}\n{formatted_file_content}\n\n"


def list_all_files(path=None, ignore_list=None):
    """
    Recursively list all file paths within the given directory, including files
    nested within sub-directories, ignoring files or directories with names
    starting with a period or matching any names in the ignore_list.

    :param path: Optional path to the directory. If not provided, uses the
    current path.
    :param ignore_list: Optional list of strings containing names to ignore.
    :return: List of strings containing file paths within the directory.
    """
    if path is None:
        path = os.getcwd()

    if ignore_list is None:
        ignore_list = []

    file_paths = []

    for root, dirs, files in os.walk(path):
        # Ignore directories starting with a period or in the ignore_list
        dirs[:] = [d for d in dirs if not d.startswith(
            '.') and d not in ignore_list]

        for file in files:
            # Ignore files starting with a period or in the ignore_list
            if not file.startswith('.') and file not in ignore_list:
                file_paths.append(os.path.join(root, file))

    return file_paths


def build_context_prefix_from_directory(path=None, ignore_list=None):
    """
    Build the context prefix string based on all the files in the
    specified (or current) directory.

    :param path: Optional path to directory. If not given, uses current path.
    :param ignore_list: Optional list of strings containing names to ignore.
    :return: context_prefix: String containing the context prefix
    """
    context_file_paths = list_all_files(path, ignore_list)
    context_prefix = build_context_prefix(context_file_paths)
    return context_prefix
