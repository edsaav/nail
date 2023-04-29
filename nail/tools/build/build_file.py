import os

from nail.core.file_editor import FileEditor
from nail.core.chat_utils import predict_code
from nail.core.context_utils import build_context_prefix


def build_file(file_path, context_file_paths=None, model=None):
    file = FileEditor(file_path)
    if not file.exists():
        file.open_editor()
    prompt = file.content()
    context_prefix = build_context_prefix(context_file_paths)
    draft_contents = predict_code(f"{context_prefix}{prompt}", model=model)
    file.apply_changes(draft_contents)
