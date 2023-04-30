from nail.core.file_editor import FileEditor
from nail.core.chat_utils import predict_code

REQUEST_SUFFIX = "Return the full modified file contents. Any non-code text should only be included as inline comments."


def debug_file(file_path, error_message, model=None):
    file = FileEditor(file_path)
    file_content = file.content()
    if error_message:
        request = f"Fix the following error message: {error_message}"
    else:
        request = "Fix any bugs in the file."
    prompt = f"Original file contents:\n```\n{file_content}\n```\n\n{request}\n{REQUEST_SUFFIX}"

    modified_contents = predict_code(prompt, model=model)
    file.apply_changes(modified_contents)
