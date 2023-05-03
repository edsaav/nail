import os

from nail.core.file_editor import FileEditor
from nail.core.prompt.context_compiler import ContextCompiler
from nail.core.chat import Chat


def build_file(file_path, context_file_paths=None, model=None):
    file = FileEditor(file_path)
    if not file.exists():
        file.open_editor()
    prompt = file.content()
    context_prefix = ContextCompiler(context_file_paths).compile_all()
    draft_contents = Chat(model).predict_code(f"{context_prefix}{prompt}")
    file.apply_changes(draft_contents)
