import os

from app.core.file_utils import read_file, apply_changes, open_editor
from app.core.chat_utils import predict_code
from app.core.context_utils import build_context_prefix


def build_file(file_path, context_file_paths=None, model=None):
    if not os.path.exists(file_path):
        open_editor(file_path)
    prompt = read_file(file_path)
    context_prefix = build_context_prefix(context_file_paths)
    draft_contents = predict_code(f"{context_prefix}{prompt}", model=model)
    apply_changes(file_path, draft_contents)
