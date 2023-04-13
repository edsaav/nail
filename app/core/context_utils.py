from app.core.file_utils import read_file

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
