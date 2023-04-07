from app.core.file_utils import read_file, write_file
from app.core.chat_utils import predict_code


def modify_file(file_path, request):
    file_content = read_file(file_path)
    prompt = f"Original file contents:\n```\n{file_content}\n```\n\nRequest: {request}\nReturn the full modified file contents."

    modified_contents = predict_code(prompt)
    write_file(file_path, modified_contents)
