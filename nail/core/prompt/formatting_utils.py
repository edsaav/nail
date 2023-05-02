# Formatting Utilities

def file_block(file_path):
    """
    Returns a formatted code block containing the contents of the file at
    the given file path.

    :param file_path: The path to the file to be formatted.
    :return: A formatted code block string containing the contents of the
    file at the given file path.
    """
    with open(file_path, "r") as file:
        file_content = file.read()
    return _format_file_block(file_path, file_content)


def _format_file_block(context_file_path, context_content):
    label = _format_file_label(context_file_path)
    formatted_file_content = f"```\n{context_content}\n```"
    return f"{label}\n{formatted_file_content}\n\n"


def _format_file_label(file_path):
    return f"[[{file_path}]]"
