from nail.core.file_editor import FileEditor
from nail.core.chat_utils import predict_code
from nail.core.context_utils import build_context_prefix


def modify_file(file_path, request, context_file_paths=None, model=None):
    file = FileEditor(file_path)
    file_content = file.content()
    target_file_context = f"Original file contents:\n```\n{file_content}\n```"
    additional_file_context = build_context_prefix(context_file_paths)
    request_text = f"Request: {request}\nReturn the full modified file contents."
    prompt = f"{additional_file_context}{target_file_context}\n\n{request_text}"

    modified_contents = predict_code(prompt, model=model)
    file.apply_changes(modified_contents)
