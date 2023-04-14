from app.core.file_utils import read_file, write_file
from app.core.chat_utils import predict_code
from app.core.context_utils import build_context_prefix


def modify_file(file_path, request, context_file_paths=None):
    file_content = read_file(file_path)
    target_file_context = f"Original file contents:\n```\n{file_content}\n```"
    additional_file_context = build_context_prefix(context_file_paths)
    request_text = f"Request: {request}\nReturn the full modified file contents."
    prompt = f"{additional_file_context}{target_file_context}\n\n{request_text}"

    modified_contents = predict_code(prompt)
    write_file(file_path, modified_contents)
