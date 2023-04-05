from core.file_utils import read_file, write_file
from core.chat_utils import predict_code

REQUEST_SUFFIX = "Return the full modified file contents. Any non-code text should only be included as inline comments."


def debug_file(file_path, error_message):
    file_content = read_file(file_path)
    if error_message:
        request = f"Fix the following error message: {error_message}"
    else:
        request = "Fix any bugs in the file."
    prompt = f"Original file contents:\n```\n{file_content}\n```\n\n{request}\n{REQUEST_SUFFIX}"

    modified_contents = predict_code(prompt)
    write_file(file_path, modified_contents)
